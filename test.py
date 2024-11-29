import asyncio

from googlesearch.news_search import search_news
from googlesearch.search import search


async def test_search():
    """测试普通搜索"""
    try:
        print("\n=== 普通搜索结果 ===")
        results = await search(
            term="python programming",
            num=10,
            lang="en"
        )

        if not results:
            print("未找到搜索结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"标题: {result.title}")
            print(f"链接: {result.url}")
            print(f"描述: {result.description}")
            if result.time:
                print(f"时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"普通搜索失败: {str(e)}")
        return False


async def test_news_search():
    """测试新闻搜索"""
    try:
        print("\n=== 新闻搜索结果 ===")
        results = await search_news(
            term="python news",
            num=5,
            lang="en"
        )

        if not results:
            print("未找到新闻结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n新闻 {i}:")
            print(f"标题: {result.title}")
            print(f"链接: {result.url}")
            print(f"描述: {result.description}")
            if result.time:
                print(f"时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"新闻搜索失败: {str(e)}")
        return False


async def main():
    """运行所有测试"""
    print("开始搜索...\n")

    # 运行搜索
    await test_search()
    await test_news_search()


if __name__ == "__main__":
    asyncio.run(main())
