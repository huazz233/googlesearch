import asyncio
from typing import List, Dict, Any, Optional
from urllib.parse import unquote

import httpx
from bs4 import BeautifulSoup
from .settings import get_random_domain, get_random_user_agent
from .models import SearchResult
from .utils import deduplicate

async def _req(
    url: str,
    headers: Dict[str, str],
    client: httpx.AsyncClient,
    term: str,
    timeout: int,
    start: int = 0,
    **kwargs: Any
) -> str:
    """
    发送搜索请求
    Send search request

    Args:
        url (str): 请求URL / Request URL
        headers (dict): 请求头 / Request headers
        client (httpx.AsyncClient): HTTP客户端 / HTTP client
        term (str): 搜索词 / Search term
        timeout (int): 超时时间 / Timeout duration
        start (int): 起始位置，用于分页 / Start position for pagination
        **kwargs: 其他参数 / Additional parameters

    Returns:
        str: 响应文本 / Response text
    """
    # Google 在 Opera Mini 模式下忽略 num 参数，每页固定返回约 10 个结果
    # Google ignores num parameter in Opera Mini mode, returns ~10 results per page
    params = {
        "q": term,
        "start": start,
        **{k: v for k, v in kwargs.items()}
    }
    headers = {**headers, "Accept": "*/*"}
    resp = await client.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout,
        follow_redirects=True,
    )
    resp.raise_for_status()
    return resp.text


async def parse_results(resp_text: str, deduplicate_results: bool) -> List[SearchResult]:
    """
    解析搜索结果 (Opera Mini UA 结构)
    Parse search results (Opera Mini UA structure)

    Args:
        resp_text (str): 响应文本 / Response text
        deduplicate_results (bool): 是否去重 / Whether to deduplicate

    Returns:
        List[SearchResult]: 搜索结果列表 / List of search results
    """
    results = []
    soup = BeautifulSoup(resp_text, "html.parser")

    # Opera Mini 返回的结构 (div.Gx5Zad)
    # Opera Mini structure (div.Gx5Zad)
    # 参考 / Reference: deedy5/ddgs
    for result in soup.find_all("div", class_="Gx5Zad"):
        result_data = _extract_result_data_opera(result)
        if result_data:
            results.append(result_data)

    if deduplicate_results:
        results = deduplicate(results)

    return results


def _extract_result_data_opera(result: BeautifulSoup) -> Optional[SearchResult]:
    """
    从搜索结果块中提取数据 (Opera Mini UA 返回的结构)
    Extract data from search result block (Opera Mini UA structure)

    参考 / Reference: deedy5/ddgs
    https://github.com/deedy5/ddgs

    Args:
        result (BeautifulSoup): 搜索结果块 / Search result block

    Returns:
        Optional[SearchResult]: 搜索结果对象或None / Search result object or None
    """
    # 查找包含 /url?q= 的链接
    # Find link containing /url?q=
    link_tag = result.find("a", href=lambda x: x and "/url?q=" in x)
    if not link_tag:
        return None

    # 提取并解码链接 URL
    # Extract and decode link URL
    href = link_tag.get("href", "")
    if "/url?q=" in href:
        # 解码 URL: /url?q=https%3A%2F%2Fwww.python.org%2F&sa=U&...
        link = unquote(href.split("/url?q=")[1].split("&")[0])
    else:
        link = href

    # 跳过非 HTTP 链接 (如 Google 内部链接)
    # Skip non-HTTP links (like Google internal links)
    if not link.startswith("http"):
        return None

    # 查找标题 (在 h3 标签内)
    # Find title (inside h3 tag)
    h3_tag = result.find("h3")
    title = ""
    if h3_tag:
        # 标题可能在嵌套的 div 中
        title = h3_tag.get_text(strip=True)

    # 查找描述 (在 class 包含 "H66NU" 或 "InXCmc" 的 div 中)
    # Find description (in div with class containing "H66NU" or "InXCmc")
    description = ""
    desc_tag = result.find("div", class_=lambda x: x and ("H66NU" in x or "InXCmc" in x))
    if desc_tag:
        description = desc_tag.get_text(strip=True)

    # 如果没有标题，尝试从链接文本获取
    # If no title, try to get from link text
    if not title and link_tag:
        title = link_tag.get_text(strip=True)

    if not title:
        return None

    return SearchResult(link, title, description)


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
    **kwargs: Any
) -> List[SearchResult]:
    """
    执行 Google 搜索（支持自动翻页）
    Perform Google search (with automatic pagination)

    Args:
        url: 搜索域名URL，默认随机选择 / Search domain URL, random by default
        headers: 请求头，默认随机User-Agent / Request headers, random User-Agent by default
        term: 搜索关键词 / Search term
        num: 返回结果数量，默认10 / Number of results to return, default 10
        lang: 搜索语言，默认en / Search language, default en
        proxy: 代理配置 / Proxy configuration
        sleep_interval: 请求间隔时间（秒）/ Request interval time (seconds)
        timeout: 超时时间 / Timeout duration
        deduplicate_results: 是否去重，默认True / Whether to deduplicate, default True
        start: 起始位置，用于手动分页 / Start position for manual pagination
        **kwargs: 其他Google搜索参数 / Additional Google search parameters

    Returns:
        List[SearchResult]: 搜索结果列表 / List of search results

    Raises:
        ValueError: 页面无响应 / No response from page
        httpx.HTTPError: HTTP请求错误 / HTTP request error
    """
    # 使用默认配置 / Use default configuration
    if url is None:
        url = get_random_domain()
    if headers is None:
        headers = {"User-Agent": get_random_user_agent()}

    kwargs["hl"] = lang
    escaped_term = term.replace(' site:', '+site:')

    client_options = {}
    if proxy:
        client_options['proxy'] = proxy

    all_results: List[SearchResult] = []
    seen_urls: set = set()
    current_start = start
    # Google 每页约返回 10 个结果
    # Google returns about 10 results per page
    results_per_page = 10
    max_pages = (num // results_per_page) + 2  # 额外请求以确保足够结果
    empty_page_count = 0

    async with httpx.AsyncClient(**client_options) as client:
        for page in range(max_pages):
            if len(all_results) >= num:
                break

            # 请求当前页
            # Request current page
            resp_text = await _req(
                url, headers, client, escaped_term,
                timeout, start=current_start, **kwargs
            )

            if not resp_text:
                break

            # 解析结果
            # Parse results
            page_results = await parse_results(resp_text, deduplicate_results=False)

            if not page_results:
                empty_page_count += 1
                if empty_page_count >= 2:  # 连续两页无结果则停止
                    break
                current_start += results_per_page
                continue

            empty_page_count = 0

            # 去重并添加到结果列表
            # Deduplicate and add to results list
            for result in page_results:
                if result.url not in seen_urls:
                    seen_urls.add(result.url)
                    all_results.append(result)
                    if len(all_results) >= num:
                        break

            current_start += results_per_page

            # 请求间隔
            # Request interval
            if sleep_interval > 0 and page < max_pages - 1:
                await asyncio.sleep(sleep_interval)

    # 最终去重（如果需要）
    # Final deduplication (if needed)
    if deduplicate_results:
        all_results = deduplicate(all_results)

    return all_results[:num]
