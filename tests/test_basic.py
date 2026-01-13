#!/usr/bin/env python3
"""
快速测试脚本 / Quick test script
运行: python -m tests.test_basic
"""
import asyncio
import re
import sys

from googlesearch import search, search_news


def extract_time(description: str) -> tuple:
    """从描述中提取时间 / Extract time from description"""
    pattern = r'(\d+\s+(?:hour|day|week|month|year)s?\s+ago)$'
    match = re.search(pattern, description, re.IGNORECASE)
    if match:
        return description[:match.start()].strip(), match.group(1)
    return description, ""


async def main():
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=== GoogleSearch-Tool 快速测试 ===\n")

    # 普通搜索
    print("1. 普通搜索 (Python, num=3)")
    results = await search(term="Python", num=3)
    for r in results:
        print(f"   - {r.title[:50]}")
    print(f"   结果: {len(results)} 条\n")

    # 新闻搜索
    print("2. 新闻搜索 (Python, num=3)")
    news = await search_news(term="Python", num=3)
    for r in news:
        _, time_str = extract_time(r.description)
        print(f"   - {r.title[:40]}... [{time_str}]")
    print(f"   结果: {len(news)} 条\n")

    # 翻页
    print("3. 翻页测试 (start=0 vs start=10)")
    p1 = await search(term="Python", num=3, start=0)
    p2 = await search(term="Python", num=3, start=10)
    overlap = len(set(r.url for r in p1) & set(r.url for r in p2))
    print(f"   Page1: {len(p1)}, Page2: {len(p2)}, 重叠: {overlap}\n")

    print("=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
