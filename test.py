import asyncio

from googlesearch.news_search import search_news
from googlesearch.search import search


async def test_search():
    """
    测试普通搜索
    Test regular search

    Returns:
        bool: 搜索是否成功 / Whether search was successful
    """
    try:
        # 代理配置示例（如需使用，请取消注释并修改代理地址）
        # Proxy configuration example (uncomment and modify if needed)
        # proxy = "http://your-proxy-host:port"

        print("\n=== 普通搜索结果 / Regular Search Results ===")
        results = await search(
            term="python programming",
            num=10,
            lang="en"
            # proxy=proxy  # 取消注释以使用代理 / Uncomment to use proxy
        )

        if not results:
            print("未找到搜索结果 / No search results found")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n结果 {i} / Result {i}:")
            print(f"标题/Title: {result.title}")
            print(f"链接/URL: {result.url}")
            print(f"描述/Description: {result.description}")
            if result.time:
                print(f"时间/Time: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"普通搜索失败 / Regular search failed: {str(e)}")
        return False


async def test_news_search():
    """
    测试新闻搜索
    Test news search

    Returns:
        bool: 搜索是否成功 / Whether search was successful
    """
    try:
        print("\n=== 新闻搜索结果 / News Search Results ===")
        results = await search_news(
            term="python news",
            num=5,
            lang="en"
            # proxy="http://your-proxy-host:port"  # 取消注释并修改代理地址 / Uncomment and modify if needed
        )

        if not results:
            print("未找到新闻结果 / No news results found")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n新闻 {i} / News {i}:")
            print(f"标题/Title: {result.title}")
            print(f"链接/URL: {result.url}")
            print(f"描述/Description: {result.description}")
            if result.time:
                print(f"时间/Time: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"新闻搜索失败 / News search failed: {str(e)}")
        return False


async def main():
    """
    运行所有测试
    Run all tests
    """
    print("开始搜索... / Starting search...\n")
    await test_search()
    await test_news_search()


if __name__ == "__main__":
    asyncio.run(main())
