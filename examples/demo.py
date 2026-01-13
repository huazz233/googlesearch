#!/usr/bin/env python3
"""
GoogleSearch-Tool 使用示例 / Usage Examples

运行 / Run: python examples/demo.py
"""
import asyncio
import re

from googlesearch import search, search_news


def extract_time(description: str) -> tuple:
    """
    从新闻描述中提取时间
    Extract time from news description

    Example: "Some news content... 2 hours ago" -> ("Some news content...", "2 hours ago")
    """
    pattern = r'(\d+\s+(?:hour|day|week|month|year)s?\s+ago)$'
    match = re.search(pattern, description, re.IGNORECASE)
    if match:
        return description[:match.start()].strip(), match.group(1)
    return description, ""


async def basic_search():
    """基本搜索 / Basic search"""
    print("=== 基本搜索 / Basic Search ===")
    results = await search(term="Python programming", num=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.title}")
        print(f"   {r.url}\n")


async def news_search():
    """新闻搜索 / News search"""
    print("=== 新闻搜索 / News Search ===")
    results = await search_news(term="artificial intelligence", num=3)
    for i, r in enumerate(results, 1):
        desc, time_str = extract_time(r.description)
        print(f"{i}. {r.title}")
        print(f"   {r.url}")
        if time_str:
            print(f"   [{time_str}]\n")
        else:
            print()


async def pagination_example():
    """断点续查 / Pagination"""
    print("=== 断点续查 / Pagination ===")
    page1 = await search(term="Python", num=3, start=0)
    page2 = await search(term="Python", num=3, start=10)

    print("Page 1:")
    for r in page1:
        print(f"  - {r.title[:50]}...")

    print("\nPage 2:")
    for r in page2:
        print(f"  - {r.title[:50]}...")

    overlap = len(set(r.url for r in page1) & set(r.url for r in page2))
    print(f"\n重叠 / Overlap: {overlap}\n")


async def time_filter_example():
    """时间过滤 / Time filter"""
    print("=== 时间过滤 / Time Filter ===")
    results = await search(term="Python news", num=3, tbs="qdr:d")
    print("Past 24 hours:")
    for r in results:
        print(f"  - {r.title[:50]}...")
    print()


async def site_search_example():
    """站点限定 / Site search"""
    print("=== 站点限定 / Site Search ===")
    results = await search(term="site:github.com python", num=3)
    for r in results:
        print(f"  - {r.title[:50]}...")
        print(f"    {r.url}\n")


async def main():
    await basic_search()
    await news_search()
    await pagination_example()
    await time_filter_example()
    await site_search_example()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
