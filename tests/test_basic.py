import asyncio
import re

from googlesearch import search, search_news


def extract_time(description: str) -> tuple[str, str]:
    """
    从描述中提取时间信息
    Extract time from description

    Returns:
        tuple: (description_without_time, time_str)
    """
    # 匹配常见时间模式：X hours ago, X days ago, X weeks ago, etc.
    pattern = r'(\d+\s+(?:hour|day|week|month|year)s?\s+ago)$'
    match = re.search(pattern, description, re.IGNORECASE)
    if match:
        time_str = match.group(1)
        desc = description[:match.start()].strip()
        return desc, time_str
    return description, ""


async def test_search():
    """测试普通搜索 / Test regular search"""
    try:
        print("\n=== 普通搜索 / Regular Search ===")
        results = await search(term="Python", num=5, lang="en")

        if not results:
            print("未找到结果 / No results")
            return False

        for i, r in enumerate(results, 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")

        return True
    except Exception as e:
        print(f"失败 / Failed: {e}")
        return False


async def test_news():
    """测试新闻搜索 / Test news search"""
    try:
        print("\n=== 新闻搜索 / News Search ===")
        results = await search_news(term="Python", num=5, lang="en")

        if not results:
            print("未找到结果 / No results")
            return False

        for i, r in enumerate(results, 1):
            # 从描述中提取时间 / Extract time from description
            desc, time_str = extract_time(r.description)
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            if time_str:
                print(f"   时间/Time: {time_str}")

        return True
    except Exception as e:
        print(f"失败 / Failed: {e}")
        return False


async def main():
    print("开始测试... / Starting tests...\n")
    s1 = await test_search()
    s2 = await test_news()
    print(f"\n普通搜索: {'OK' if s1 else 'FAIL'}")
    print(f"新闻搜索: {'OK' if s2 else 'FAIL'}")


if __name__ == "__main__":
    asyncio.run(main())
