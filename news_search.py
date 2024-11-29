import asyncio

import httpx
from bs4 import BeautifulSoup

from googlesearch.config.config import Config
from googlesearch.models import SearchResult
from googlesearch.search import _req
from googlesearch.utils import deduplicate


async def parse_news_results(resp_text, deduplicate_results):
    results = []
    soup = BeautifulSoup(resp_text, "html.parser")

    search_container = soup.find("div", {"id": "search"})
    if search_container:
        result_blocks = search_container.find_all("div", attrs={"class": "SoaBEf"})
        for result in result_blocks:
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
    
    Args:
        url: 搜索域名URL，默认随机选择
        headers: 请求头，默认随机User-Agent
        term: 搜索关键词
        num: 返回结果数量，默认100
        lang: 搜索语言，默认en
        proxy: 代理配置
        sleep_interval: 请求间隔时间
        timeout: 超时时间
        deduplicate_results: 是否去重
        **kwargs: 其他Google搜索参数
    """
    # 使用默认配置
    if url is None:
        url = Config.get_random_domain()
    if headers is None:
        headers = {"User-Agent": Config.get_random_user_agent()}

    kwargs["tbm"] = "nws"
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
