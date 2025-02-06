# GooglSearch-Tool

**GooglSearch-Tool** is a Python library for performing Google searches and retrieving search results. It supports dynamic query parameters, result deduplication, and custom proxy configuration.

[![GitHub stars](https://img.shields.io/github/stars/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/issues)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)

[简体中文](README_ZH.md) | English

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [Configuration](#configuration)
- [Packaging](#packaging)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Community Support](#community-support)

## Features

- Support for Google search
- Configurable query parameters (including time range)
- Result deduplication based on title, URL, and summary
- Custom proxy support
- Search results include title, link, description, and time information
- Random domain selection for requests to prevent access restrictions
- Random User-Agent header selection
- Manual update and save of latest User-Agent and Google domain lists (functions and save location in `/config/data` directory)

## Installation

Install `googlesearch-tool` via `pip`:

```bash
pip install googlesearch-tool
```

## Quick Start

Here's a basic example of using the GooglSearch-Tool library:

```python
import asyncio
from googlesearch.search import search
from googlesearch.news_search import search_news

async def test_search():
    """Test regular search"""
    try:
        """
        Proxy Configuration Notes:
        1. Without proxy: Simply delete or comment out the proxies configuration
        2. With proxy: Uncomment and modify the proxy address
        """
        # Proxy configuration example (uncomment and modify if needed)
        # proxies = {
        #     "http://": "http://your-proxy-host:port",
        #     "https://": "http://your-proxy-host:port"
        # }
         
        print("\n=== Regular Search Results ===")
        results = await search(
            term="python programming",
            num=10,
            lang="en"
        )

        if not results:
            print("No search results found")
            return False

        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Title: {result.title}")
            print(f"URL: {result.url}")
            print(f"Description: {result.description}")
            if result.time:
                print(f"Time: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"Regular search failed: {str(e)}")
        return False

async def test_news_search():
    """Test news search"""
    try:
        print("\n=== News Search Results ===")
        results = await search_news(
            term="python news",
            num=5,
            lang="en"
        )

        if not results:
            print("No news results found")
            return False

        for i, result in enumerate(results, 1):
            print(f"\nNews {i}:")
            print(f"Title: {result.title}")
            print(f"URL: {result.url}")
            print(f"Description: {result.description}")
            if result.time:
                print(f"Time: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"News search failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_search())
    asyncio.run(test_news_search())
```

### Parameters

- `url`: Random Google domain obtained via `Config.get_random_domain()`
- `headers`: Request headers containing random User-Agent
- `term`: Search query string
- `num`: Number of results to retrieve
- `tbs`: Time range parameter
  - `qdr:h` - Past hour
  - `qdr:d` - Past day
  - `qdr:w` - Past week
  - `qdr:m` - Past month
  - `qdr:y` - Past year
- `proxies`: Proxy configuration (optional)
- `timeout`: Request timeout in seconds

### Result Object

Each search result object contains the following fields:

- `link`: Result URL
- `title`: Result title
- `description`: Result description
- `time_string`: Result time information (if available)

## Advanced Usage

### Getting Random Domains and Headers

To avoid request restrictions, the library provides functionality to get random Google search domains and User-Agents:

```python
from googlesearch.config.config import Config

# Get random Google search domain
url = Config.get_random_domain()
print(url)  # Example output: https://www.google.ge/search

# Get random User-Agent
headers = {"User-Agent": Config.get_random_user_agent()}
print(headers)  # Example output: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.1.7760.206 Safari/537.36'}
```

### Domain and User-Agent Updates

Domain lists and User-Agent lists are stored in the `config/data` directory:
- `all_domain.txt`: Contains all available Google search domains
- `user_agents.txt`: Contains the latest Chrome User-Agent list

To update these lists:
1. Run `fetch_and_save_user_domain.py` to update the domain list
2. Run `fetch_and_save_user_agents.py` to update the User-Agent list

## Configuration

### Why do my requests always time out?

Please check your network connection and proxy settings. Ensure that your proxy is configured correctly and that the target site is not blocked.

### How do I make more complex queries?

You can use Google search's advanced syntax (such as `site:`, `filetype:`, etc.) to construct more complex query strings.

### How do I handle request failures or exceptions?

Please ensure proper exception handling in your requests and check the error logs for more information. You can refer to the [httpx documentation](https://www.python-httpx.org/) for more information about exception handling.

## Contributing

We welcome community members to participate in project development! Here are several ways to contribute:

### Star ⭐ This Project
If you find this project helpful, please show your support by clicking the Star button in the top right corner!

### Submit Issues
Found a bug or have a feature suggestion? Please submit an [Issue](https://github.com/huazz233/googlesearch/issues)!
- 🐛 Bug reports: Please describe the issue in detail with steps to reproduce
- 💡 Feature suggestions: Please explain the use case and expected behavior

### Pull Requests
Want to contribute code? We welcome PRs!

1. Fork this repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit changes: `git commit -am 'Add some feature'`
4. Push branch: `git push origin feature/your-feature-name`
5. Submit a Pull Request

We will carefully review each PR and provide timely feedback.

## Community Support

- 📫 Email: [huazz233@163.com](mailto:huazz233@163.com)
- 💬 Issue Feedback: [GitHub Issues](https://github.com/huazz233/googlesearch/issues)
- 📖 Development Docs: [Wiki](https://github.com/huazz233/googlesearch/wiki)
- 👥 Discussion: [Discussions](https://github.com/huazz233/googlesearch/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 

## Advanced Search Syntax

> For more detailed information about Google search operators and advanced search techniques, please visit [Google Search Help](https://support.google.com/websearch/answer/2466433).

### Basic Search Operators

Here are some commonly used search operators. Note: Don't include spaces between the operator and search terms:

- **Exact Match Search**: Use quotes around phrases, e.g., `"exact phrase"`
- **Site Search**: `site:domain.com keywords`
- **Exclude Terms**: Use minus sign to exclude words, e.g., `python -snake`
- **File Type**: `filetype:pdf keywords`
- **Title Search**: `intitle:keywords`
- **URL Search**: `inurl:keywords`
- **Multiple Conditions**: `site:domain.com filetype:pdf keywords`

### Time Range Parameters (tbs)

The search function supports the following time range parameters:

```python
tbs = {
    "qdr:h",  # Results from the past hour
    "qdr:d",  # Results from the past day
    "qdr:w",  # Results from the past week
    "qdr:m",  # Results from the past month
    "qdr:y"   # Results from the past year
}
```

### Other Search Parameters

```python
params = {
    "hl": "en",        # Interface language (e.g., en, zh-CN)
    "lr": "lang_en",   # Search results language
    "safe": "active",  # Safe search setting ("active" enables safe search)
    "start": 0,        # Starting position for results (for pagination)
    "num": 100,        # Number of results to return (max 100)
}
```

### Advanced Search Examples

```python
# Search for PDF files on specific website
term = "site:example.com filetype:pdf python programming"

# Search for news within specific time range
term = "python news site:cnn.com"
tbs = "qdr:d"  # Results from past 24 hours

# Exact match in title
term = 'intitle:"machine learning" site:arxiv.org'

# Exclude specific content
term = "python programming -beginner -tutorial site:github.com"
```

### Search Result Filtering

Search results can be filtered by the following types:
- Web
- News
- Images
- Videos

Our library provides dedicated functions for different types of searches:
```python
# Regular web search
results = await search(...)

# News search
news_results = await search_news(...)
```

### Search Tips

1. **Using Multiple Conditions**
   ```python
   # Search across multiple specific sites
   term = "site:edu.gov OR site:org.gov machine learning"
   ```

2. **Using Wildcards**
   ```python
   # Use asterisk as wildcard
   term = "python * programming"
   ```

3. **Using Number Ranges**
   ```python
   # Search within specific year range
   term = "python programming 2020..2024"
   ```

4. **Related Terms Search**
   ```python
   # Use tilde for related terms
   term = "~programming tutorials"
   ```

For more detailed information about Google search operators and advanced search techniques, please visit [Google Search Help](https://support.google.com/websearch/answer/2466433). 
