import asyncio

import httpx
from bs4 import BeautifulSoup
from googlesearch.config.config import base_url, user_agent
from googlesearch.models import SearchResult
from googlesearch.utils import deduplicate, clean_description


async def _req(client, term, num_results, lang, timeout, safe, **kwargs):
    url = base_url
    headers = {"User-Agent": user_agent}
    params = {
        "q": term,
        "num": num_results,
        "hl": lang,
        "start": 0,
        "safe": safe,
        "biw": 1692,  # 指定窗口高度，宽度
        "bih": 856,
        **{k: v for k, v in kwargs.items()}
    }
    # print(f"请求 URL: {url}")
    # print(f"请求参数: {params}")
    resp = await client.get(url, headers=headers, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.text


async def parse_results(resp_text, deduplicate_results):
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


async def search(term, num=20, lang="en", proxies=None, sleep_interval=0, timeout=5, safe="active",
                 deduplicate_results=False, **kwargs):
    escaped_term = term.replace(' site:', '+site:')
    client_options = {}
    if proxies:
        client_options['proxies'] = proxies
    # client_options['verify'] = False
    async with httpx.AsyncClient(**client_options) as client:
        resp_text = await _req(client, escaped_term, num, lang, timeout, safe, **kwargs)
        if not resp_text:
            raise ValueError("页面无响应")
        results = await parse_results(resp_text, deduplicate_results)
        await asyncio.sleep(sleep_interval)
        return results
