"""
Google 新闻搜索模块
Google News Search Module

使用 Opera Mini User-Agent 绕过 JavaScript 检测
Uses Opera Mini User-Agent to bypass JavaScript detection
"""
import asyncio
from typing import List, Dict, Any, Optional

import httpx
from .settings import get_random_domain, get_random_user_agent
from .models import SearchResult
from .search import _req, parse_results
from .utils import deduplicate


async def search_news(
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
    执行 Google 新闻搜索（支持自动翻页）
    Perform Google News search (with automatic pagination)

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
        List[SearchResult]: 新闻搜索结果列表 / List of news search results
    """
    # 使用默认配置 / Use default configuration
    if url is None:
        url = get_random_domain()
    if headers is None:
        headers = {"User-Agent": get_random_user_agent()}

    # 添加新闻搜索参数 / Add news search parameter
    kwargs["tbm"] = "nws"
    kwargs["hl"] = lang
    escaped_term = term.replace(' site:', '+site:')

    client_options = {}
    if proxy:
        client_options['proxy'] = proxy

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
                timeout, start=current_start, **kwargs
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
