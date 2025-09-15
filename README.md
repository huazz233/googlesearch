# GoogleSearch-Tool

> **⚠️ IMPORTANT NOTICE**
>
> **Google Search functionality is currently unavailable. News Search is temporarily available.**
>
> **For official Google Search API, please visit: https://developers.google.cn/custom-search/v1/libraries?hl=en**

**GoogleSearch-Tool** is a powerful Python library for performing Google searches and retrieving search results programmatically. It features dynamic query parameters, intelligent result deduplication, custom proxy support, and automatic domain rotation to avoid rate limiting.

[![GitHub stars](https://img.shields.io/github/stars/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/issues)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/googlesearch-tool.svg)](https://badge.fury.io/py/googlesearch-tool)

[简体中文](README_ZH.md) | **English**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Parameters](#api-parameters)
- [Advanced Usage](#advanced-usage)
- [Search Syntax](#search-syntax)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Community Support](#community-support)

## Features

- **Google Search Support**: Perform both regular web searches and news searches
- **Advanced Query Parameters**: Support for time ranges, language settings, and Google search operators
- **Intelligent Deduplication**: Remove duplicate results based on title, URL, and content
- **Proxy Support**: Full proxy configuration support for bypassing restrictions
- **Anti-Detection**:
  - Random Google domain rotation from 167+ domains
  - Random User-Agent rotation from latest Chrome versions
  - Automatic request throttling
- **Comprehensive Results**: Extract title, URL, description, and timestamp information
- **Auto-Updates**: Automated daily updates of domains and User-Agent lists via GitHub Actions
- **Easy Integration**: Simple async/await API with comprehensive error handling

## Installation

Install the latest version via pip:

```bash
pip install --upgrade googlesearch-tool
```

**PyPI Package**: [https://pypi.org/project/googlesearch-tool/](https://pypi.org/project/googlesearch-tool/)

### Requirements

- Python 3.7+
- httpx
- beautifulsoup4
- anyio
- socksio (for SOCKS proxy support)

## Quick Start

### Basic Web Search

```python
import asyncio
from googlesearch.search import search

async def basic_search():
    """Perform a basic Google search"""
    results = await search(
        term="python programming",
        num=10,
        lang="en"
    )

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Description: {result.description}")
        if result.time:
            print(f"   Time: {result.time}")
        print()

# Run the search
asyncio.run(basic_search())
```

### News Search

```python
import asyncio
from googlesearch.news_search import search_news

async def news_search():
    """Search for news articles"""
    results = await search_news(
        term="artificial intelligence",
        num=5,
        lang="en"
    )

    for result in results:
        print(f"📰 {result.title}")
        print(f"🔗 {result.url}")
        print(f"📝 {result.description}")
        print(f"⏰ {result.time}")
        print("-" * 50)

asyncio.run(news_search())
```

### Advanced Search with Proxy

```python
import asyncio
from googlesearch.search import search

async def advanced_search():
    """Advanced search with proxy and time filtering"""
    results = await search(
        term="site:github.com machine learning",
        num=20,
        lang="en",
        tbs="qdr:m",  # Past month
        proxy="http://your-proxy-host:port",  # Optional
        timeout=15
    )

    for result in results:
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Description: {result.description[:100]}...")
        print()

asyncio.run(advanced_search())
```

## API Parameters

### Search Function Parameters

- `term`: Search query string
- `num`: Number of results to retrieve (default 10, max 100)
- `lang`: Search language (e.g., "en", "zh-CN")
- `tbs`: Time range parameter
  - `qdr:h` - Past hour
  - `qdr:d` - Past day
  - `qdr:w` - Past week
  - `qdr:m` - Past month
  - `qdr:y` - Past year
- `proxy`: Proxy configuration (optional)
- `timeout`: Request timeout in seconds
- `deduplicate_results`: Whether to remove duplicates (default False)

### Result Object Properties

Each search result contains the following properties:

- `url`: Result URL
- `title`: Result title
- `description`: Result description
- `time`: Time information (if available)

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
print(headers)
```

### Domain and User-Agent Management

Domain lists and User-Agent lists are stored in the `config/data` directory:
- `all_domain.txt`: Contains 167+ available Google search domains
- `user_agents.txt`: Contains the latest Chrome User-Agent list

#### Update Methods

**1. Manual Update of Individual Files**
```bash
cd config/data
python fetch_and_save_user_domain.py    # Update domain list
python fetch_and_save_user_agents.py    # Update User-Agent list
python check_domains.py                 # Check domain availability
```

**2. Manual Update of All Data**
```bash
python config/data/update_data.py
```

**3. Automatic Update via GitHub Actions**
- Runs daily at UTC 0:00
- Manual trigger available on GitHub Actions page
- Automatic commit and push of changes
- View logs and status on Actions page

Update process:
1. Updates User-Agent list
2. Updates Google domain list
3. Checks domain availability
4. Commits changes if any

## Search Syntax

### Basic Search Operators

Common search operators (no spaces between operator and search terms):

- **Exact Match**: Use quotes around phrases, e.g., `"exact phrase"`
- **Site Search**: `site:domain.com keywords`
- **Exclude Terms**: Use minus sign, e.g., `python -snake`
- **File Type**: `filetype:pdf keywords`
- **Title Search**: `intitle:keywords`
- **URL Search**: `inurl:keywords`
- **Multiple Conditions**: `site:domain.com filetype:pdf keywords`

### Time Range Parameters

```python
tbs_options = {
    "qdr:h",  # Past hour
    "qdr:d",  # Past day
    "qdr:w",  # Past week
    "qdr:m",  # Past month
    "qdr:y"   # Past year
}
```

### Advanced Search Examples

```python
# Search PDF files on specific website
term = "site:example.com filetype:pdf python programming"

# Search news within time range
term = "python news site:cnn.com"
tbs = "qdr:d"  # Past 24 hours

# Exact match in title
term = 'intitle:"machine learning" site:arxiv.org'

# Exclude specific content
term = "python programming -beginner -tutorial site:github.com"
```

## Configuration

### Proxy Setup

1. **Without Proxy**: Remove or comment out proxy parameters
2. **With Proxy**: Set proxy parameter to your proxy server URL

### Common Issues

**Request Timeouts**: Check network connection and proxy settings

**Complex Queries**: Use Google search operators (`site:`, `filetype:`, etc.)

**Error Handling**: Implement proper exception handling and check logs

## Contributing

We welcome contributions! Here's how you can help:

### ⭐ Star the Project
If you find this project helpful, please star it to show your support!

### 🐛 Report Issues
Found a bug or have a feature request? [Submit an issue](https://github.com/huazz233/googlesearch/issues)

### 🔧 Submit Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a Pull Request

## Community Support

- 📧 **Email**: [huazz233@163.com](mailto:huazz233@163.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/huazz233/googlesearch/issues)
- 📚 **Documentation**: [Wiki](https://github.com/huazz233/googlesearch/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/huazz233/googlesearch/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> For more detailed information about Google search operators and advanced search techniques, visit [Google Search Help](https://support.google.com/websearch/answer/2466433).
