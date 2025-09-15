"""
GoogleSearch-Tool: A powerful Python library for performing Google searches

This package provides functionality for:
- Regular Google web searches
- Google news searches  
- Advanced search parameters and filtering
- Proxy support and anti-detection features
- Intelligent result deduplication

Basic usage:
    import asyncio
    from googlesearch import search, search_news
    
    async def main():
        # Regular search
        results = await search("python programming", num=10)
        for result in results:
            print(f"{result.title}: {result.url}")
            
        # News search
        news = await search_news("artificial intelligence", num=5)
        for article in news:
            print(f"{article.title}: {article.url}")
    
    asyncio.run(main())

For more advanced usage, see the documentation and examples.
"""

__version__ = "1.1.4"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"
__pypi_url__ = "https://pypi.org/project/googlesearch-tool/"

# Import main functions for easy access
from .search import search
from .news_search import search_news
from .models import SearchResult

# Define what gets imported with "from googlesearch import *"
__all__ = [
    'search',
    'search_news',
    'SearchResult',
    '__version__',
    '__pypi_url__',
]
