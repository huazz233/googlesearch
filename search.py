import asyncio

import httpx
from bs4 import BeautifulSoup
from googlesearch.config.config import Config
from googlesearch.models import SearchResult
from googlesearch.utils import deduplicate, clean_description


async def _req(url, headers, client, term, num_results, timeout, **kwargs):
    """
    发送搜索请求
    Send search request

    Args:
        url (str): 请求URL / Request URL
        headers (dict): 请求头 / Request headers
        client (httpx.AsyncClient): HTTP客户端 / HTTP client
        term (str): 搜索词 / Search term
        num_results (int): 结果数量 / Number of results
        timeout (int): 超时时间 / Timeout duration
        **kwargs: 其他参数 / Additional parameters

    Returns:
        str: 响应文本 / Response text
    """
    params = {
        "q": term,
        "num": num_results,
        "start": 0,
        "biw": 1692,  # 指定窗口高度 / Specify window height
        "bih": 856,   # 指定窗口宽度 / Specify window width
        **{k: v for k, v in kwargs.items()}
    }
    resp = await client.get(url, headers=headers, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.text


async def parse_results(resp_text, deduplicate_results):
    """
    解析搜索结果
    Parse search results

    Args:
        resp_text (str): 响应文本 / Response text
        deduplicate_results (bool): 是否去重 / Whether to deduplicate

    Returns:
        List[SearchResult]: 搜索结果列表 / List of search results
    """
    results = []
    soup = BeautifulSoup(resp_text, "html.parser")

    result_block = soup.find_all("div", attrs={"class": "g"})
    if not result_block:
        result_block = soup.find_all("div", attrs={"class": "tF2Cxc"})

    for result in result_block:
        link = result.find("a", href=True)
        title = result.find("h3")

        # 获取描述框
        description_box = (
                result.find("div", {"style": "-webkit-line-clamp:2"}) or
                result.find("span", {"class": "aCOpRe"}) or
                result.find("span", {"class": "ITZIwc"})  # 视频
        )

        # 获取时间字符串
        time_span = result.find("span", attrs={"class": "LEwnzc Sqrs4e"})
        if time_span:
            time_string = time_span.find("span").text
        else:
            alternative_time_span = result.find("span", attrs={"class": "gqF9jc"})
            if alternative_time_span:
                time_string = (alternative_time_span.find_all("span"))[1].text
            else:
                time_string = "未知时间"  # 或者其他默认值

        # 获取描述文本
        description = None
        if description_box:
            description = clean_description(description_box.text)

        # 添加结果到列表
        if link and title and description:
            results.append(SearchResult(link["href"], title.text, description, time_string))

    if deduplicate_results:
        results = deduplicate(results)

    return results


async def search(
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
    执行 Google 搜索
    Perform Google search
    
    Args:
        url: 搜索域名URL，默认随机选择 / Search domain URL, random by default
        headers: 请求头，默认随机User-Agent / Request headers, random User-Agent by default
        term: 搜索关键词 / Search term
        num: 返回结果数量，默认100 / Number of results to return, default 100
        lang: 搜索语言，默认en / Search language, default en
        proxy: 代理配置 / Proxy configuration
        sleep_interval: 请求间隔时间 / Request interval time
        timeout: 超时时间 / Timeout duration
        deduplicate_results: 是否去重 / Whether to deduplicate
        **kwargs: 其他Google搜索参数 / Additional Google search parameters
    """
    # 使用默认配置 / Use default configuration
    if url is None:
        url = Config.get_random_domain()
    if headers is None:
        headers = {"User-Agent": Config.get_random_user_agent()}

    kwargs["hl"] = lang
    escaped_term = term.replace(' site:', '+site:')
    
    client_options = {}
    if proxy:
        client_options['proxy'] = proxy

    async with httpx.AsyncClient(**client_options) as client:
        resp_text = await _req(url, headers, client, escaped_term, num, timeout, **kwargs)
        if not resp_text:
            raise ValueError("No response from page")
        results = await parse_results(resp_text, deduplicate_results)
        await asyncio.sleep(sleep_interval)
        return results
