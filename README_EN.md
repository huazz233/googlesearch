# GooglSearch-Tool

**GooglSearch-Tool** is a Python library for performing Google searches and retrieving search results. It supports dynamic query parameters, result deduplication, and custom proxy configuration.

[![GitHub stars](https://img.shields.io/github/stars/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/issues)
[![GitHub license](https://img.shields.io/github/license/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/blob/master/LICENSE)

[简体中文](README.md) | English

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
from googlesearch.config.config import Config
from googlesearch.search import search
from googlesearch.news_search import search_news

async def main():
    # Configure proxy (optional)
    proxies = {
        "http://": "http://127.0.0.1:10809",
        "https://": "http://127.0.0.1:10809"
    }

    # Get random domain and User-Agent
    url = Config.get_random_domain()
    headers = {"User-Agent": Config.get_random_user_agent()}
    
    # Regular search
    results = await search(
        url=url,
        headers=headers,
        term="python site:cnn.com",
        num=100,
        tbs="qdr:h",  # Results from the past hour
        proxies=proxies
    )
    
    # Print search results
    for result in results:
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Description: {result.description}")
        print(f"Time: {result.time}\n")

    # News search
    news_results = await search_news(
        url=url,
        headers=headers,
        term="python site:cnn.com",
        num=100,
        tbs="qdr:d",  # Results from the past day
        proxy=proxies
    )
    
    # Print news search results
    for result in news_results:
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Description: {result.description}")
        print(f"Time: {result.time}\n")

if __name__ == "__main__":
    asyncio.run(main())
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
Found a bug or have a feature suggestion? Please submit an [Issue](https://github.com/yourusername/googlesearch-tool/issues)!
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
- 💬 Issue Feedback: [GitHub Issues](https://github.com/yourusername/googlesearch-tool/issues)
- 📖 Development Docs: [Wiki](https://github.com/yourusername/googlesearch-tool/wiki)
- 👥 Discussion: [Discussions](https://github.com/yourusername/googlesearch-tool/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 