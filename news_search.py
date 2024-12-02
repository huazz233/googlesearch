import asyncio

import httpx
from bs4 import BeautifulSoup
from googlesearch.config.config import Config
from googlesearch.models import SearchResult
from googlesearch.search import _req
from googlesearch.utils import deduplicate


async def parse_news_results(resp_text, deduplicate_results):
    """
    解析新闻搜索结果
    Parse news search results

    Args:
        resp_text (str): 响应文本 / Response text
        deduplicate_results (bool): 是否去重 / Whether to deduplicate

    Returns:
        List[SearchResult]: 新闻搜索结果列表 / List of news search results
    """
    results = []
    soup = BeautifulSoup(resp_text, "html.parser")

    # 查找新闻容器 / Find news container
    search_container = soup.find("div", {"id": "search"})
    if search_container:
        # 查找所有新闻块 / Find all news blocks
        result_blocks = search_container.find_all("div", attrs={"class": "SoaBEf"})
        for result in result_blocks:
            # 提取链接、描述、标题和时间 / Extract link, description, title and time
            link_tag = result.find("a", href=True)
            description_tag = result.find("div", {"class": "n0jPhd ynAwRc MBeuO nDgy9d"})
            title_tag = result.find("div", {"class": "GI74Re nDgy9d"}) or result.find("div", {"class": "SoaBEf"})
            time_tag = result.find("div", {"class": "OSrXXb rbYSKb LfVVr"})

            if link_tag and title_tag and description_tag:
                description = title_tag.text.strip().replace('\n', '')
                title = description_tag.text
                url = link_tag["href"]
                time = time_tag.text if time_tag else None
                results.append(SearchResult(url, title, description, time))

    if deduplicate_results:
        results = deduplicate(results)

    return results


async def search_news(
    url=None,
    headers=None,
    term="",
    num=100,
    lang="en",
    proxy=None,
    sleep_interval=0,
    timeout=10,
    deduplicate_results=False,
    **kwargs
):
    """
    执行 Google 新闻搜索
    Perform Google News search
    
    Args:
        url (str, optional): 搜索域名URL / Search domain URL
        headers (dict, optional): 请求头 / Request headers
        term (str): 搜索关键词 / Search term
        num (int): 返回结果数量 / Number of results to return
        lang (str): 搜索语言 / Search language
        proxy (dict, optional): 代理配置 / Proxy configuration
        sleep_interval (int): 请求间隔时间 / Request interval time
        timeout (int): 超时时间 / Timeout duration
        deduplicate_results (bool): 是否去重 / Whether to deduplicate
        **kwargs: 其他Google搜索参数 / Additional Google search parameters

    Returns:
        List[SearchResult]: 新闻搜索结果列表 / List of news search results

    Raises:
        ValueError: 页面无响应时抛出 / Raised when page has no response
    """
    # 使用默认配置 / Use default configuration
    if url is None:
        url = Config.get_random_domain()
    if headers is None:
        headers = {"User-Agent": Config.get_random_user_agent()}

    kwargs["tbm"] = "nws"  # 新闻搜索参数 / News search parameter
    kwargs["hl"] = lang
    escaped_term = term.replace(' site:', '+site:')
    
    client_options = {}
    if proxy:
        client_options['proxies'] = proxy

    async with httpx.AsyncClient(**client_options, verify=True) as client:
        resp_text = await _req(url, headers, client, escaped_term, num, timeout, **kwargs)
        if not resp_text:
            raise ValueError("No response from page")
        results = await parse_news_results(resp_text, deduplicate_results)
        await asyncio.sleep(sleep_interval)
        return results
