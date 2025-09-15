#!/usr/bin/env python3
"""
GoogleSearch-Tool 使用示例
GoogleSearch-Tool Usage Example

这个文件展示了如何使用 googlesearch-tool 包进行搜索
This file demonstrates how to use the googlesearch-tool package for searching

安装方法 / Installation:
pip install googlesearch-tool

PyPI 地址 / PyPI URL:
https://pypi.org/project/googlesearch-tool/
"""

import asyncio
from googlesearch import search, search_news


async def basic_search_example():
    """基本搜索示例 / Basic search example"""
    print("🔍 基本搜索示例 / Basic Search Example")
    print("=" * 50)
    
    try:
        results = await search(
            term="python programming",
            num=5,
            lang="en"
        )
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.title}")
            print(f"   🔗 {result.url}")
            print(f"   📝 {result.description[:100]}...")
            print()
            
    except Exception as e:
        print(f"❌ 搜索失败 / Search failed: {e}")


async def news_search_example():
    """新闻搜索示例 / News search example"""
    print("\n📰 新闻搜索示例 / News Search Example")
    print("=" * 50)
    
    try:
        results = await search_news(
            term="artificial intelligence",
            num=3,
            lang="en"
        )
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 📰 {result.title}")
            print(f"   🔗 {result.url}")
            print(f"   📝 {result.description[:100]}...")
            if result.time:
                print(f"   ⏰ {result.time}")
            print()
            
    except Exception as e:
        print(f"❌ 新闻搜索失败 / News search failed: {e}")


async def advanced_search_example():
    """高级搜索示例 / Advanced search example"""
    print("\n🚀 高级搜索示例 / Advanced Search Example")
    print("=" * 50)
    
    try:
        # 使用搜索操作符 / Using search operators
        results = await search(
            term="site:github.com python machine learning",
            num=3,
            lang="en",
            tbs="qdr:m"  # 过去一个月 / Past month
        )
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 🔧 {result.title}")
            print(f"   🔗 {result.url}")
            print(f"   📝 {result.description[:100]}...")
            print()
            
    except Exception as e:
        print(f"❌ 高级搜索失败 / Advanced search failed: {e}")


async def main():
    """运行所有示例 / Run all examples"""
    print("🎯 GoogleSearch-Tool 示例程序")
    print("🎯 GoogleSearch-Tool Example Program")
    print(f"📦 PyPI: https://pypi.org/project/googlesearch-tool/")
    print("=" * 60)
    
    await basic_search_example()
    await news_search_example()
    await advanced_search_example()
    
    print("\n✅ 所有示例运行完成！/ All examples completed!")
    print("📚 更多用法请参考 README.md / For more usage, see README.md")


if __name__ == "__main__":
    asyncio.run(main())
