# GoogleSearch-Tool

**GoogleSearch-Tool** is a Python library for performing Google searches programmatically.

Uses Opera Mini User-Agent to bypass Google's JavaScript detection (Jan 2025+).

[![PyPI version](https://badge.fury.io/py/googlesearch-tool.svg)](https://badge.fury.io/py/googlesearch-tool)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)

[简体中文](README_ZH.md) | **English**

## Features

- **Web Search & News Search**: Regular and news search support
- **Automatic Pagination**: Auto-fetch multiple pages via `start` parameter
- **Proxy Support**: Full proxy configuration
- **Anti-Detection**: Opera Mini User-Agent bypass, random domain rotation

## Installation

```bash
pip install --upgrade googlesearch-tool
```

**Requirements**: Python 3.7+, httpx, beautifulsoup4

## Quick Start

### Basic Search

```python
import asyncio
from googlesearch import search

async def main():
    results = await search(term="python programming", num=10)
    for r in results:
        print(f"{r.title}")
        print(f"  {r.url}")
        print(f"  {r.description[:80]}...")

asyncio.run(main())
```

### News Search

```python
import asyncio
from googlesearch import search_news

async def main():
    results = await search_news(term="artificial intelligence", num=5)
    for r in results:
        print(f"{r.title} - {r.url}")

asyncio.run(main())
```

### Pagination (Resume Search)

```python
# First page
page1 = await search(term="Python", num=10, start=0)

# Resume from position 10
page2 = await search(term="Python", num=10, start=10)
```

## API Parameters

### search() / search_news()

| Parameter | Description | Default |
|-----------|-------------|---------|
| `term` | Search query | Required |
| `num` | Number of results | 10 |
| `lang` | Language code | "en" |
| `start` | Start position (pagination) | 0 |
| `proxy` | Proxy URL | None |
| `timeout` | Request timeout (seconds) | 10 |
| `sleep_interval` | Delay between requests | 0 |
| `deduplicate_results` | Remove duplicates | True |

### SearchResult Object

| Property | Description |
|----------|-------------|
| `url` | Result URL |
| `title` | Result title |
| `description` | Result description |

## Advanced Usage

### With Proxy

```python
results = await search(
    term="python",
    num=10,
    proxy="http://your-proxy:port"
)
```

### Time Range Filter

```python
results = await search(
    term="python news",
    tbs="qdr:d"  # Past day
)
```

Time range options:
- `qdr:h` - Past hour
- `qdr:d` - Past day
- `qdr:w` - Past week
- `qdr:m` - Past month
- `qdr:y` - Past year

### Site-Specific Search

```python
results = await search(term="site:github.com python")
```

## Reference

- Opera Mini UA bypass: [deedy5/ddgs](https://github.com/deedy5/ddgs)

## License

MIT License
