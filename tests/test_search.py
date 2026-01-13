"""
GoogleSearch-Tool 测试模块
Test module for GoogleSearch-Tool
"""
import asyncio
import unittest

from googlesearch import search, search_news
from googlesearch.models import SearchResult


class TestSearchResult(unittest.TestCase):
    """测试 SearchResult 数据模型"""

    def test_create_result(self):
        """测试创建搜索结果对象"""
        result = SearchResult(
            url="https://example.com",
            title="Example Title",
            description="Example Description"
        )
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Example Title")
        self.assertEqual(result.description, "Example Description")

    def test_strip_whitespace(self):
        """测试自动去除空白字符"""
        result = SearchResult(
            url="  https://example.com  ",
            title="  Title  ",
            description="  Desc  "
        )
        self.assertEqual(result.url, "https://example.com")
        self.assertEqual(result.title, "Title")
        self.assertEqual(result.description, "Desc")

    def test_to_dict(self):
        """测试转换为字典"""
        result = SearchResult("https://example.com", "Title", "Desc")
        d = result.to_dict()
        self.assertEqual(d["url"], "https://example.com")
        self.assertEqual(d["title"], "Title")
        self.assertEqual(d["description"], "Desc")


class TestBasicSearch(unittest.TestCase):
    """测试基本搜索功能"""

    def test_search_returns_results(self):
        """测试搜索返回结果"""
        async def run():
            results = await search(term="Python", num=5)
            return results

        results = asyncio.run(run())
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], SearchResult)

    def test_search_result_has_required_fields(self):
        """测试搜索结果包含必要字段"""
        async def run():
            results = await search(term="Python", num=3)
            return results

        results = asyncio.run(run())
        for r in results:
            self.assertTrue(r.url.startswith("http"))
            self.assertGreater(len(r.title), 0)

    def test_search_num_parameter(self):
        """测试 num 参数控制结果数量"""
        async def run():
            results = await search(term="Python programming", num=5)
            return results

        results = asyncio.run(run())
        self.assertLessEqual(len(results), 5)


class TestNewsSearch(unittest.TestCase):
    """测试新闻搜索功能"""

    def test_news_search_returns_results(self):
        """测试新闻搜索返回结果"""
        async def run():
            results = await search_news(term="technology", num=5)
            return results

        results = asyncio.run(run())
        self.assertGreater(len(results), 0)


class TestPagination(unittest.TestCase):
    """测试翻页功能"""

    def test_pagination_returns_different_results(self):
        """测试不同 start 值返回不同结果"""
        async def run():
            page1 = await search(term="Python tutorial", num=5, start=0)
            page2 = await search(term="Python tutorial", num=5, start=10)
            return page1, page2

        page1, page2 = asyncio.run(run())
        urls1 = {r.url for r in page1}
        urls2 = {r.url for r in page2}
        # 两页结果应该不同
        self.assertNotEqual(urls1, urls2)


class TestTimeFilter(unittest.TestCase):
    """测试时间范围过滤"""

    def test_tbs_parameter_affects_results(self):
        """测试 tbs 参数影响搜索结果"""
        async def run():
            results_hour = await search(term="Python news", num=5, tbs="qdr:h")
            results_year = await search(term="Python news", num=5, tbs="qdr:y")
            return results_hour, results_year

        results_hour, results_year = asyncio.run(run())
        urls_hour = {r.url for r in results_hour}
        urls_year = {r.url for r in results_year}
        # 不同时间范围应返回不同结果
        self.assertNotEqual(urls_hour, urls_year)


class TestSiteSearch(unittest.TestCase):
    """测试站点限定搜索"""

    def test_site_operator(self):
        """测试 site: 操作符"""
        async def run():
            results = await search(term="site:github.com python", num=5)
            return results

        results = asyncio.run(run())
        # 结果应该来自 github.com
        github_count = sum(1 for r in results if "github.com" in r.url)
        self.assertGreater(github_count, 0)


if __name__ == "__main__":
    unittest.main()
