"""
GoogleSearch-Tool: A Python library for performing Google searches

Uses Opera Mini User-Agent to bypass JavaScript detection.

Basic usage:
    import asyncio
    from googlesearch import search

    async def main():
        results = await search("python programming", num=10)
        for result in results:
            print(f"{result.title}: {result.url}")

    asyncio.run(main())

For more advanced usage, see the documentation and examples.
"""

__version__ = "2.0.0"
__author__ = "huazz233"
__email__ = "huazz233@163.com"
__license__ = "MIT"
__pypi_url__ = "https://pypi.org/project/googlesearch-tool/"

# Import main functions for easy access
from .search import search
from .news import search_news
from .models import SearchResult

# Define what gets imported with "from googlesearch import *"
__all__ = [
    'search',
    'search_news',
    'SearchResult',
    '__version__',
    '__pypi_url__',
]
