import asyncio

import httpx
from bs4 import BeautifulSoup

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


async def search_news(term, num=20, lang="en", proxy=None, sleep_interval=0, timeout=5, safe="active",
                      deduplicate_results=False, **kwargs):
    kwargs["tbm"] = "nws"
    escaped_term = term.replace(' site:', '+site:')
    client_options = {}
    if proxy:
        client_options['proxies'] = proxy

    async with httpx.AsyncClient(**client_options, verify=True) as client:
        resp_text = await _req(client, escaped_term, num, lang, timeout, safe, **kwargs)
        if not resp_text:
            raise ValueError("页面无响应")
        results = await parse_news_results(resp_text, deduplicate_results)
        await asyncio.sleep(sleep_interval)
        return results
