import asyncio
import random
from typing import List, Dict, Any, Optional
from urllib.parse import unquote, urlparse, urlunparse

import httpx
from bs4 import BeautifulSoup, Tag

from .settings import (
    GOOGLE_COOKIES,
    get_random_domain,
    get_random_user_agent,
    iter_stable_domains,
)
from .models import SearchResult
from .utils import deduplicate


# 触发重试的状态码 — Google 在限流/反爬时常返回 403 或 429
# Status codes that trigger retry — Google often uses 403 / 429 for rate limiting
_RETRY_STATUS = {403, 429, 503}
_MAX_ATTEMPTS = 4

# 解析时需要丢弃的 Google 内部链接前缀(AI Overview "Learn more" 等噪声)
# Internal Google links to discard when parsing (AI Overview noise etc.)
_NOISE_HOSTS = (
    "support.google.com/websearch",
    "policies.google.com",
    "accounts.google.com",
)


def _swap_domain(url: str, alternatives: List[str], exclude: set) -> str:
    """从备用池中选一个未试过的域名,保留原 URL 的 path/query."""
    parsed = urlparse(url)
    pool = [u for u in alternatives if urlparse(u).netloc not in exclude]
    if not pool:
        return url
    new = urlparse(random.choice(pool))
    return urlunparse(parsed._replace(netloc=new.netloc, scheme=new.scheme))


async def _req(
    url: str,
    headers: Dict[str, str],
    client: httpx.AsyncClient,
    term: str,
    timeout: int,
    start: int = 0,
    **kwargs: Any,
) -> str:
    """
    发送搜索请求。403/429 自动指数退避重试,并切换备用域名。
    Send a search request. On 403/429 it retries with exponential backoff
    AND swaps to an alternative domain from the stable pool to dodge
    per-domain rate limits.
    """
    params = {"q": term, "start": start, **kwargs}
    headers = {**headers, "Accept": "*/*"}
    alternatives = iter_stable_domains()
    tried_hosts: set = set()
    current_url = url

    last_exc: Optional[Exception] = None
    for attempt in range(_MAX_ATTEMPTS):
        tried_hosts.add(urlparse(current_url).netloc)
        try:
            resp = await client.get(
                current_url,
                headers=headers,
                params=params,
                cookies=GOOGLE_COOKIES,
                timeout=timeout,
                follow_redirects=True,
            )
            if resp.status_code in _RETRY_STATUS and attempt < _MAX_ATTEMPTS - 1:
                await asyncio.sleep(0.3 + 0.4 * attempt)
                current_url = _swap_domain(current_url, alternatives, tried_hosts)
                continue
            resp.raise_for_status()
            return resp.text
        except httpx.HTTPStatusError as e:
            last_exc = e
            if e.response.status_code not in _RETRY_STATUS or attempt == _MAX_ATTEMPTS - 1:
                raise
            await asyncio.sleep(0.3 + 0.4 * attempt)
            current_url = _swap_domain(current_url, alternatives, tried_hosts)
        except (httpx.TimeoutException, httpx.TransportError) as e:
            last_exc = e
            if attempt == _MAX_ATTEMPTS - 1:
                raise
            await asyncio.sleep(0.3 + 0.4 * attempt)

    if last_exc:
        raise last_exc
    return ""


def _decode_google_href(href: str) -> str:
    """解码 Google 的 /url?q=... 跳转链接 / Decode Google /url?q=... redirect."""
    if "/url?q=" in href:
        return unquote(href.split("/url?q=", 1)[1].split("&", 1)[0])
    return href


def _is_real_result(link: str) -> bool:
    """判断是否是真实的 http(s) 外链,且不属于 Google 内部噪声链接."""
    if not link.startswith("http"):
        return False
    return not any(noise in link for noise in _NOISE_HOSTS)


def _extract_lynx(block: Tag) -> Optional[SearchResult]:
    """Lynx UA 路径: div.ezO2md → span.CVA68e (title) + span.FrIlee (desc)."""
    link_tag = block.find("a", href=True)
    if not link_tag:
        return None
    link = _decode_google_href(link_tag["href"])
    if not _is_real_result(link):
        return None
    title_tag = link_tag.find("span", class_="CVA68e") or link_tag.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else link_tag.get_text(strip=True)
    desc_tag = block.find("span", class_="FrIlee")
    desc = desc_tag.get_text(strip=True) if desc_tag else ""
    if not title:
        return None
    return SearchResult(link, title, desc)


def _extract_opera_mini(block: Tag) -> Optional[SearchResult]:
    """Opera Mini UA 路径: div.Gx5Zad → h3 + div.H66NU / div.InXCmc."""
    link_tag = block.find("a", href=lambda x: x and "/url?q=" in x)
    if not link_tag:
        return None
    link = _decode_google_href(link_tag.get("href", ""))
    if not _is_real_result(link):
        return None
    h3 = block.find("h3")
    title = h3.get_text(strip=True) if h3 else link_tag.get_text(strip=True)
    desc_tag = block.find("div", class_=lambda x: x and ("H66NU" in x or "InXCmc" in x))
    desc = desc_tag.get_text(strip=True) if desc_tag else ""
    if not title:
        return None
    return SearchResult(link, title, desc)


def _extract_generic(block: Tag) -> Optional[SearchResult]:
    """
    通用兜底: 找带 h3 的 <a>,描述取容器内剩余文本前若干字符
    Generic fallback: find <a> containing h3, take leftover text as snippet.
    """
    link_tag = block.find("a", href=True)
    if not link_tag:
        return None
    href = link_tag["href"]
    link = _decode_google_href(href)
    if not _is_real_result(link):
        return None
    h3 = block.find("h3")
    title = h3.get_text(strip=True) if h3 else link_tag.get_text(strip=True)[:120]
    if not title:
        return None
    block_text = block.get_text(" ", strip=True)
    desc = block_text.replace(title, "", 1).strip()[:280]
    return SearchResult(link, title, desc)


def _parse_with(soup: BeautifulSoup, finder, extractor) -> List[SearchResult]:
    """运行一组 finder/extractor 提取结果."""
    out: List[SearchResult] = []
    for block in finder(soup):
        item = extractor(block)
        if item:
            out.append(item)
    return out


async def parse_results(resp_text: str, deduplicate_results: bool) -> List[SearchResult]:
    """
    多策略解析降级链 / Multi-strategy parser with fallback chain.

    顺序 / Priority:
      1. Lynx 路径:  div.ezO2md            (Nv7-GitHub master)
      2. data-hveid 路径: div[data-hveid] 含 h3 (ddgs 当前 / 桌面新结构)
      3. Opera Mini 路径: div.Gx5Zad        (旧轻量 SERP)
      4. 兜底:      任何含 h3 的 a 的祖先 div
    """
    soup = BeautifulSoup(resp_text, "html.parser")

    strategies = [
        # 2026-05 实测主路径: Opera Mini UA → div.Gx5Zad
        # Empirically primary path (2026-05): Opera Mini UA → div.Gx5Zad
        (lambda s: s.find_all("div", class_="Gx5Zad"), _extract_opera_mini),
        # Lynx 路径(Nv7-GitHub master 用法,2026-05 已被 Google 拒)
        # Lynx path (still in Nv7-GitHub master, blocked by Google in 2026-05)
        (lambda s: s.find_all("div", class_="ezO2md"), _extract_lynx),
        # 桌面新结构兜底 / Desktop new-structure fallback
        (
            lambda s: [
                b for b in s.find_all("div", attrs={"data-hveid": True}) if b.find("h3")
            ],
            _extract_generic,
        ),
    ]

    results: List[SearchResult] = []
    for finder, extractor in strategies:
        results = _parse_with(soup, finder, extractor)
        if results:
            break

    if not results:
        # 最终兜底: 所有 h3 的最近祖先 div
        # Last resort: nearest div ancestor of every h3
        seen_blocks = set()
        last_resort_blocks = []
        for h3 in soup.find_all("h3"):
            parent = h3.find_parent("div")
            if parent is not None and id(parent) not in seen_blocks:
                seen_blocks.add(id(parent))
                last_resort_blocks.append(parent)
        results = [_extract_generic(b) for b in last_resort_blocks]
        results = [r for r in results if r]

    if deduplicate_results:
        results = deduplicate(results)
    return results


async def search(
    url: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    term: str = "",
    num: int = 10,
    lang: str = "en",
    proxy: Optional[str] = None,
    sleep_interval: float = 0,
    timeout: int = 10,
    deduplicate_results: bool = True,
    start: int = 0,
    **kwargs: Any,
) -> List[SearchResult]:
    """
    执行 Google 搜索（支持自动翻页）
    Perform Google search (with automatic pagination)
    """
    if url is None:
        url = get_random_domain()
    if headers is None:
        headers = {"User-Agent": get_random_user_agent()}

    kwargs["hl"] = lang
    escaped_term = term.replace(" site:", "+site:")

    client_options: Dict[str, Any] = {}
    if proxy:
        client_options["proxy"] = proxy

    all_results: List[SearchResult] = []
    seen_urls: set = set()
    current_start = start
    results_per_page = 10
    max_pages = (num // results_per_page) + 2
    empty_page_count = 0

    async with httpx.AsyncClient(**client_options) as client:
        for page in range(max_pages):
            if len(all_results) >= num:
                break

            resp_text = await _req(
                url, headers, client, escaped_term,
                timeout, start=current_start, **kwargs,
            )
            if not resp_text:
                break

            page_results = await parse_results(resp_text, deduplicate_results=False)

            if not page_results:
                empty_page_count += 1
                if empty_page_count >= 2:
                    break
                current_start += results_per_page
                continue

            empty_page_count = 0

            for result in page_results:
                if result.url not in seen_urls:
                    seen_urls.add(result.url)
                    all_results.append(result)
                    if len(all_results) >= num:
                        break

            current_start += results_per_page

            if sleep_interval > 0 and page < max_pages - 1:
                await asyncio.sleep(sleep_interval)

    if deduplicate_results:
        all_results = deduplicate(all_results)

    return all_results[:num]
