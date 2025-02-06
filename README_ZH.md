# GooglSearch-Tool

**GooglSearch-Tool** is a Python library for performing Google searches and retrieving search results. It supports dynamic query parameters, result deduplication, and custom proxy configuration.

**GooglSearch-Tool** 是一个 Python 库，用于进行 Google 搜索并获取搜索结果。支持动态查询参数、结果去重以及自定义代理配置。

[![GitHub stars](https://img.shields.io/github/stars/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/issues)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)

[English](README.md) | 简体中文

## Table of Contents / 目录

- [Features / 特性](#features)
- [Installation / 安装](#installation)
- [Quick Start / 快速开始](#quick-start)
- [Advanced Usage / 高级用法](#advanced-usage)
- [Configuration / 配置说明](#configuration)
- [Packaging / 打包说明](#packaging)
- [FAQ / 常见问题](#faq)
- [Contributing / 参与贡献](#contributing)
- [Community Support / 社区支持](#community-support)

## Features

- Support for Google search
- Configurable query parameters (including time range)
- Result deduplication based on title, URL, and summary
- Custom proxy support
- Search results include title, link, description, and time information
- Random domain selection for requests to prevent access restrictions
- Random User-Agent header selection
- Manual update and save of latest User-Agent and Google domain lists (functions and save locations in `/config/data` directory)

## 特性

- 支持 Google 搜索
- 可配置的查询参数（包括时间范围）
- 根据标题、URL 和摘要进行结果去重
- 支持自定义代理
- 搜索结果包括标题、链接、描述和时间信息
- 使用随机域名进行请求，防止访问受限
- 随机选择 User-Agent 请求头
- 手动更新并保存最新的 User-Agent 和 Google 域名列表（函数与保存位置在 `/config/data` 目录）

## Installation

Install `googlesearch-tool` via `pip`:

通过 `pip` 安装 `googlesearch-tool`：

```bash
pip install googlesearch-tool
```

## Quick Start

Here's a basic example of using the GooglSearch-Tool library:

以下是使用 GooglSearch-Tool 库的基本示例：

### Basic Example / 基础示例

```python
import asyncio
from googlesearch.search import search
from googlesearch.news_search import search_news

async def test_search():
    """Test regular search / 测试普通搜索"""
    try:
        """
        Proxy configuration notes / 代理配置说明：
        1. Without proxy: Delete or comment out proxies configuration
           不使用代理：直接删除或注释掉 proxies 配置
        2. With proxy: Uncomment and modify proxy address
           使用代理：取消注释并修改代理地址
        """
        # Proxy configuration example (uncomment and modify if needed)
        # 代理配置示例（如需使用，请取消注释并修改代理地址）
        # proxies = {
        #     "http://": "http://your-proxy-host:port",
        #     "https://": "http://your-proxy-host:port"
        # }
         
        print("\n=== Regular Search Results / 普通搜索结果 ===")
        results = await search(
            term="python programming",
            num=10,
            lang="en"
        )

        if not results:
            print("No search results found / 未找到搜索结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\nResult {i} / 结果 {i}:")
            print(f"Title / 标题: {result.title}")
            print(f"Link / 链接: {result.url}")
            print(f"Description / 描述: {result.description}")
            if result.time:
                print(f"Time / 时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"Regular search failed / 普通搜索失败: {str(e)}")
        return False

async def test_news_search():
    """Test news search / 测试新闻搜索"""
    try:
        print("\n=== News Search Results / 新闻搜索结果 ===")
        results = await search_news(
            term="python news",
            num=5,
            lang="en"
        )

        if not results:
            print("No news results found / 未找到新闻结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\nNews {i} / 新闻 {i}:")
            print(f"Title / 标题: {result.title}")
            print(f"Link / 链接: {result.url}")
            print(f"Description / 描述: {result.description}")
            if result.time:
                print(f"Time / 时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"News search failed / 新闻搜索失败: {str(e)}")
        return False

async def main():
    """Run all tests / 运行所有测试"""
    print("Starting search... / 开始搜索...\n")
    await test_search()
    await test_news_search()

if __name__ == "__main__":
    asyncio.run(main())
```

### Proxy Configuration / 代理配置说明

1. **Without Proxy / 不使用代理**
   - Delete or comment out proxies configuration
   - Make sure proxies/proxy parameters in search functions are also commented out
   - 直接删除或注释掉 proxies 配置
   - 确保搜索函数中的 proxies/proxy 参数也被注释掉

2. **With Proxy / 使用代理**
   - Uncomment proxies configuration
   - Modify proxy address to your actual proxy server address
   - 取消注释 proxies 配置
   - 修改代理地址为您的实际代理服务器地址

### Parameter Description / 参数说明

- `url`: Random Google domain obtained via `Config.get_random_domain()`
  通过 `Config.get_random_domain()` 获取的随机 Google 域名
- `headers`: Request headers containing random User-Agent
  包含随机 User-Agent 的请求头
- `term`: Search query string
  搜索查询字符串
- `num`: Number of results to retrieve
  要获取的结果数量
- `tbs`: Time range parameter
  时间范围参数
  - `qdr:h` - Past hour / 过去一小时
  - `qdr:d` - Past day / 过去一天
  - `qdr:w` - Past week / 过去一周
  - `qdr:m` - Past month / 过去一月
  - `qdr:y` - Past year / 过去一年
- `proxies`: Proxy configuration (optional)
  代理配置（可选）
- `timeout`: Request timeout in seconds
  请求超时时间（秒）

### Result Object / 结果对象

Each search result object contains the following fields:
每个搜索结果的对象包含以下字段：

- `link`: Result URL / 结果的 URL
- `title`: Result title / 结果的标题
- `description`: Result description / 结果的描述
- `time_string`: Result time information (if available) / 结果的时间信息（如果有）

## Advanced Usage / 高级用法

### Getting Random Domains and Headers / 获取随机域名和请求头

To avoid request restrictions, the library provides functionality to get random Google search domains and User-Agents:
为了避免请求被限制，库提供了获取随机 Google 搜索域名和随机 User-Agent 的功能：

```python 
from googlesearch.config.config import Config

# Get random Google search domain / 获取随机 Google 搜索域名
url = Config.get_random_domain()
print(url)  # Example output / 输出示例: https://www.google.ge/search

# Get random User-Agent / 获取随机 User-Agent
headers = {"User-Agent": Config.get_random_user_agent()}
print(headers)  # Example output / 输出示例: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.1.7760.206 Safari/537.36'}
```

### Domain and User-Agent Updates / 域名和 User-Agent 更新

域名列表和 User-Agent 列表存储在 `config/data` 目录下：
- `all_domain.txt`: 包含所有可用的 Google 搜索域名
- `user_agents.txt`: 包含最新的 Chrome User-Agent 列表

更新这些列表有三种方式：

#### 1. 手动更新单个文件
- 运行 `fetch_and_save_user_domain.py` 更新域名列表
- 运行 `fetch_and_save_user_agents.py` 更新 User-Agent 列表
- 运行 `check_domains.py` 检查域名可用性

#### 2. 手动更新所有数据
运行 `update_data.py` 脚本可以一次性更新所有数据：
```bash
python config/data/update_data.py
```

#### 3. GitHub Actions 自动更新
我们配置了 GitHub Actions 工作流来自动更新数据：
- 每天 UTC 0:00（北京时间 8:00）自动运行
- 可以在 GitHub 仓库的 Actions 页面手动触发更新
- 更新后会自动提交变更并推送到仓库
- 可以在 Actions 页面查看更新日志和状态

自动更新流程：
1. 更新 User-Agent 列表
2. 更新 Google 域名列表
3. 检查域名可用性
4. 如有变更，自动提交并推送到仓库

## Advanced Search Syntax / 高级搜索语法

> For more detailed Google search operators and advanced search tips, visit [Google Search Help](https://support.google.com/websearch/answer/2466433).
> 更多详细的 Google 搜索运算符和高级搜索技巧，请访问 [Google 搜索帮助](https://support.google.com/websearch/answer/2466433)。

### Basic Search Operators / 基础搜索运算符

Here are some commonly used search operators. Note that there should be no space between operators and search terms:
以下是一些常用的搜索运算符，使用时请注意运算符和搜索词之间不要有空格：

- **Exact Match Search / 精确匹配搜索**: Use quotes around phrases, e.g., `"exact phrase"`
  使用引号包围词组，如 `"exact phrase"`
- **Site Search / 站内搜索**: `site:domain.com keywords`
- **Exclude Terms / 排除特定词**: Use minus sign to exclude words, e.g., `china -snake`
  使用减号排除词，如 `china -snake`
- **File Type / 文件类型**: `filetype:pdf keywords`
- **Title Search / 标题搜索**: `intitle:keywords`
- **URL Search / URL搜索**: `inurl:keywords`
- **Multiple Conditions / 多个条件**: `site:domain.com filetype:pdf keywords`

### Time Range Parameters (tbs) / 时间范围参数 (tbs)

The search function supports the following time range parameters:
搜索函数支持以下时间范围参数：

```python
tbs = {
    "qdr:h",  # Results from the past hour / 过去一小时内的结果
    "qdr:d",  # Results from the past day / 过去一天内的结果
    "qdr:w",  # Results from the past week / 过去一周内的结果
    "qdr:m",  # Results from the past month / 过去一月内的结果
    "qdr:y"   # Results from the past year / 过去一年内的结果
}
```

### Other Search Parameters / 其他搜索参数

```python
params = {
    "hl": "zh-CN",     # Interface language (e.g., zh-CN, en) / 界面语言（例如：zh-CN, en）
    "lr": "lang_zh",   # Search result language / 搜索结果语言
    "safe": "active",  # Safe search setting ("active" enables safe search) / 安全搜索设置（"active"启用安全搜索）
    "start": 0,        # Result start position (for pagination) / 结果起始位置（分页用）
    "num": 100,        # Number of results to return (max 100) / 返回结果数量（最大100）
}
```

### Advanced Search Examples / 高级搜索示例

```python
# Search PDF files on a specific website / 在特定网站中搜索PDF文件
term = "site:example.com filetype:pdf china programming"

# Search news within a specific time range / 搜索特定时间范围内的新闻
term = "china news site:cnn.com"
tbs = "qdr:d"  # Results from past 24 hours / 过去24小时内的结果

# Exact match phrase in title / 精确匹配标题中的短语
term = 'intitle:"machine learning" site:arxiv.org'

# Exclude specific content / 排除特定内容
term = "china programming -beginner -tutorial site:github.com"
```

## Configuration / 配置说明

### Why is my request always timing out?

Please check your network connection and proxy settings. Ensure that the proxy configuration is correct and that the target website is not blocked.

### How to perform more complex queries?

You can use Google search advanced syntax (e.g., `site:`, `filetype:` etc.) to construct more complex query strings.

### How to handle request failure or exceptions?

Please ensure appropriate exception handling in your request and check error logs for more information. You can refer to [httpx documentation](https://www.python-httpx.org/) for more information about exception handling.

## Packaging / 打包说明

When packaging with PyInstaller, ensure that configuration files are correctly included. Below are the packaging steps and notes:

使用 PyInstaller 打包时，需要确保配置文件被正确包含。以下是打包步骤和注意事项：

### 1. Create spec file

```bash
pyi-makespec --onefile your_script.py
```

### 2. Modify spec file

You need to add datas parameter in spec file to ensure necessary configuration files are included:
需要在 spec 文件中添加 datas 参数，确保包含必要的配置文件：

```python 
# your_script.spec
a = Analysis(
    ['your_script.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Add configuration files
        ('googlesearch/config/data/all_domain.txt', 'googlesearch/config/data'),
        ('googlesearch/config/data/user_agents.txt', 'googlesearch/config/data'),
    ],
    # ... other configurations ...
)
```

### 3. Use spec file to package

```bash
pyinstaller your_script.spec
```

### 4. Verify packaging result

Run packaged program to ensure configuration files are correctly loaded:
运行打包后的程序，确保能正确读取配置文件：
```python 
from googlesearch.config.config import Config

# Test configuration files loading
url = Config.get_random_domain()
headers = {"User-Agent": Config.get_random_user_agent()}
```

If you encounter file not found errors, please check spec file path configuration.
如果出现文件未找到的错误，请检查 spec 文件中的路径配置是否正确。

## FAQ / 常见问题

### Why is my request always timing out?

Please check your network connection and proxy settings. Ensure that the proxy configuration is correct and that the target website is not blocked.

### How to perform more complex queries?

You can use Google search advanced syntax (e.g., `site:` etc.) to construct more complex query strings.

### How to handle request failure or exceptions?

Please ensure appropriate exception handling in your request and check error logs for more information. You can refer to [httpx documentation](https://www.python-httpx.org/) for more information about exception handling.

## Contributing / 参与贡献

We welcome community members to participate in project construction! Below are several ways to participate:
我们非常欢迎社区成员参与项目建设！以下是几种参与方式：

### Star ⭐ This Project
If you find this project helpful, please click the Star button in the upper right corner to support us!
如果您觉得这个项目对您有帮助，欢迎点击右上角的 Star 按钮支持我们！

### Submit Issue 
Found a bug or new feature suggestion? Welcome to submit [Issue](https://github.com/huazz233/googlesearch/issues)!
- 🐛 Bug Feedback: Please describe the problem phenomenon and reproduction steps
- 💡 Feature Suggestion: Please explain the new feature usage scenario and expected effect

### Pull Request
Want to contribute code to the project? Very welcome to submit PR!

1. Fork this repository
2. Create new branch: `git checkout -b feature/your-feature-name`
3. Commit changes: `git commit -am 'Add some feature'`
4. Push branch: `git push origin feature/your-feature-name`
5. Submit Pull Request

We will review each PR carefully and provide timely feedback.
我们会认真审查每一个 PR，并提供及时反馈。

## Community Support / 社区支持

- 📫 Email Contact: [huazz233@163.com](mailto:huazz233@163.com)
- 💬 Problem Feedback: [GitHub Issues](https://github.com/huazz233/googlesearch/issues)
- 📖 Development Documentation: [Wiki](https://github.com/huazz233/googlesearch/wiki)
- 👥 Discussion Area: [Discussions](https://github.com/huazz233/googlesearch/discussions)

## License

This project uses MIT License - View [LICENSE](LICENSE) for details
