import asyncio

from googlesearch.news_search import search_news
from googlesearch.search import search


def clean_splitter_description(description, splitter):
    time_parts = description.split(splitter, 1)
    if len(time_parts) > 1:
        return time_parts[1].strip()
    return description


async def main():
    # proxies = None  # 用户可以在这里传入代理配置，例如 {"http://": "http://proxy.example.com", "https://": "https://proxy.example.com"}

    proxies = {
        "http://": "http://127.0.0.1:10809",
        "https://": "http://127.0.0.1:10809"
    }
    # 普通搜索
    results = await search(term="xi site:www.theguardian.com", num=100, tbs="qdr:h", proxies=proxies)
    print("普通搜索结果:")
    if results:
        for result in results:
            print(
                f"标题: {result.title}\n链接: {result.url}\n"
                f"摘要: {clean_splitter_description(result.description, 'ago — ')}\n时间: {result.time}\n")
    else:
        print("没有找到相关结果。")

    print("\n=================================\n")

    # 新闻搜索
    news_results = await search_news(term="xi site:www.theguardian.com", num=100, tbs="qdr:d", proxy=proxies)
    print("\n新闻搜索结果:")
    if news_results:
        for result in news_results:
            print(f"标题: {result.title}\n链接: {result.url}\n摘要: {result.description}\n时间: {result.time}\n")
    else:
        print("没有找到相关新闻。")


if __name__ == "__main__":
    asyncio.run(main())
