# GoogleSearch-Tool

**GoogleSearch-Tool** 是一个用于执行 Google 搜索的 Python 库。

使用 Opera Mini User-Agent 绕过 Google 的 JavaScript 检测（2025年1月起）。

[![PyPI version](https://badge.fury.io/py/googlesearch-tool.svg)](https://badge.fury.io/py/googlesearch-tool)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)

**简体中文** | [English](README.md)

## 功能特性

- **网页搜索 & 新闻搜索**：支持普通搜索和新闻搜索
- **自动翻页**：通过 `start` 参数自动获取多页结果
- **代理支持**：完整的代理配置
- **反检测**：Opera Mini User-Agent 绕过，随机域名轮换

## 安装

```bash
pip install --upgrade googlesearch-tool
```

**依赖**：Python 3.7+, httpx, beautifulsoup4

## 快速开始

### 基本搜索

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

### 新闻搜索

```python
import asyncio
from googlesearch import search_news

async def main():
    results = await search_news(term="人工智能", num=5)
    for r in results:
        print(f"{r.title} - {r.url}")

asyncio.run(main())
```

### 翻页（断点续查）

```python
# 第一页
page1 = await search(term="Python", num=10, start=0)

# 从第10条继续
page2 = await search(term="Python", num=10, start=10)
```

## API 参数

### search() / search_news()

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `term` | 搜索关键词 | 必填 |
| `num` | 返回结果数量 | 10 |
| `lang` | 语言代码 | "en" |
| `start` | 起始位置（翻页） | 0 |
| `proxy` | 代理地址 | None |
| `timeout` | 请求超时（秒） | 10 |
| `sleep_interval` | 请求间隔 | 0 |
| `deduplicate_results` | 去重 | True |

### SearchResult 对象

| 属性 | 说明 |
|------|------|
| `url` | 结果链接 |
| `title` | 结果标题 |
| `description` | 结果描述 |

## 高级用法

### 使用代理

```python
results = await search(
    term="python",
    num=10,
    proxy="http://your-proxy:port"
)
```

### 时间范围过滤

```python
results = await search(
    term="python news",
    tbs="qdr:d"  # 过去一天
)
```

时间范围选项：
- `qdr:h` - 过去一小时
- `qdr:d` - 过去一天
- `qdr:w` - 过去一周
- `qdr:m` - 过去一个月
- `qdr:y` - 过去一年

### 站点限定搜索

```python
results = await search(term="site:github.com python")
```

## 参考

- Opera Mini UA 方案：[deedy5/ddgs](https://github.com/deedy5/ddgs)

## 许可证

MIT License
