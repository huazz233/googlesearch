#!/usr/bin/env python3
"""
GoogleSearch-Tool 使用示例 / Usage Example

安装 / Install: pip install googlesearch-tool
PyPI: https://pypi.org/project/googlesearch-tool/
"""
import asyncio
from googlesearch import search, search_news


async def basic_search():
    """基本搜索 / Basic search"""
    print("=== 基本搜索 / Basic Search ===")
    results = await search(term="Python programming", num=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.title}")
        print(f"   {r.url}")


async def news_search():
    """新闻搜索 / News search"""
    print("\n=== 新闻搜索 / News Search ===")
    results = await search_news(term="artificial intelligence", num=3)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r.title}")
        print(f"   {r.url}")


async def pagination_example():
    """断点续查 / Pagination example"""
    print("\n=== 断点续查 / Pagination ===")
    # 第一页 / First page
    page1 = await search(term="Python", num=3, start=0)
    print("Page 1:")
    for r in page1:
        print(f"  - {r.title[:40]}...")

    # 第二页 / Second page
    page2 = await search(term="Python", num=3, start=10)
    print("Page 2:")
    for r in page2:
        print(f"  - {r.title[:40]}...")


async def main():
    await basic_search()
    await news_search()
    await pagination_example()
    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
