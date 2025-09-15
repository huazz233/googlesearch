# GoogleSearch-Tool

> **⚠️ 重要提示**
>
> **Google 搜索功能目前不可用，新闻搜索暂时可用。**
>
> **如需使用官方 Google 搜索 API，请访问：https://developers.google.cn/custom-search/v1/libraries?hl=en**

**GoogleSearch-Tool** 是一个强大的 Python 库，用于程序化执行 Google 搜索并获取搜索结果。它具有动态查询参数、智能结果去重、自定义代理支持和自动域名轮换等功能，有效避免访问限制。

[![GitHub stars](https://img.shields.io/github/stars/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/issues)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/googlesearch-tool.svg)](https://badge.fury.io/py/googlesearch-tool)

[English](README.md) | **简体中文**

## 目录

- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [API 参数](#api-参数)
- [高级用法](#高级用法)
- [搜索语法](#搜索语法)
- [配置管理](#配置管理)
- [常见问题](#常见问题)
- [参与贡献](#参与贡献)
- [社区支持](#社区支持)

## 特性

- **Google 搜索支持**：支持常规网页搜索和新闻搜索
- **高级查询参数**：支持时间范围、语言设置和 Google 搜索运算符
- **智能去重**：基于标题、URL 和内容智能去除重复结果
- **代理支持**：完整的代理配置支持，绕过访问限制
- **反检测机制**：
  - 167+ 个 Google 域名随机轮换
  - 最新 Chrome 版本 User-Agent 随机轮换
  - 自动请求节流控制
- **全面的结果信息**：提取标题、URL、描述和时间戳信息
- **自动更新**：通过 GitHub Actions 每日自动更新域名和 User-Agent 列表
- **易于集成**：简单的 async/await API，完善的错误处理

## 安装

通过 pip 安装最新版本：

```bash
pip install --upgrade googlesearch-tool
```

### 系统要求

- Python 3.7+
- httpx
- beautifulsoup4
- anyio
- socksio（SOCKS 代理支持）

## 快速开始

### 基础网页搜索

```python
import asyncio
from googlesearch.search import search

async def basic_search():
    """执行基础 Google 搜索"""
    results = await search(
        term="Python 编程",
        num=10,
        lang="zh-CN"
    )
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   链接: {result.url}")
        print(f"   描述: {result.description}")
        if result.time:
            print(f"   时间: {result.time}")
        print()

# 运行搜索
asyncio.run(basic_search())
```

### 新闻搜索

```python
import asyncio
from googlesearch.news_search import search_news

async def news_search():
    """搜索新闻文章"""
    results = await search_news(
        term="人工智能",
        num=5,
        lang="zh-CN"
    )
    
    for result in results:
        print(f"📰 {result.title}")
        print(f"🔗 {result.url}")
        print(f"📝 {result.description}")
        print(f"⏰ {result.time}")
        print("-" * 50)

asyncio.run(news_search())
```

### 高级搜索（含代理）

```python
import asyncio
from googlesearch.search import search

async def advanced_search():
    """高级搜索，包含代理和时间过滤"""
    results = await search(
        term="site:github.com 机器学习",
        num=20,
        lang="zh-CN",
        tbs="qdr:m",  # 过去一个月
        proxy="http://your-proxy-host:port",  # 可选
        timeout=15
    )
    
    for result in results:
        print(f"标题: {result.title}")
        print(f"链接: {result.url}")
        print(f"描述: {result.description[:100]}...")
        print()

asyncio.run(advanced_search())
```

## API 参数

### 搜索函数参数

- `term`: 搜索关键词
- `num`: 返回结果数量（默认 10，最大 100）
- `lang`: 搜索语言（如 "zh-CN", "en"）
- `tbs`: 时间范围参数
  - `qdr:h` - 过去一小时
  - `qdr:d` - 过去一天
  - `qdr:w` - 过去一周
  - `qdr:m` - 过去一个月
  - `qdr:y` - 过去一年
- `proxy`: 代理配置（可选）
- `timeout`: 请求超时时间（秒）
- `deduplicate_results`: 是否去重（默认 False）

### 结果对象属性

每个搜索结果包含以下属性：

- `url`: 结果链接
- `title`: 结果标题
- `description`: 结果描述
- `time`: 时间信息（如果可用）

## 高级用法

### 获取随机域名和请求头

为了避免请求限制，库提供了获取随机 Google 搜索域名和 User-Agent 的功能：

```python
from googlesearch.config.config import Config

# 获取随机 Google 搜索域名
url = Config.get_random_domain()
print(url)  # 示例输出: https://www.google.ge/search

# 获取随机 User-Agent
headers = {"User-Agent": Config.get_random_user_agent()}
print(headers)
```

### 域名和 User-Agent 更新

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

## 搜索语法

### 基础搜索运算符

以下是一些常用的搜索运算符，使用时请注意运算符和搜索词之间不要有空格：

- **精确匹配搜索**: 使用引号包围词组，如 `"精确短语"`
- **站内搜索**: `site:domain.com 关键词`
- **排除特定词**: 使用减号排除词，如 `Python -蛇`
- **文件类型**: `filetype:pdf 关键词`
- **标题搜索**: `intitle:关键词`
- **URL搜索**: `inurl:关键词`
- **多个条件**: `site:domain.com filetype:pdf 关键词`

### 时间范围参数

```python
tbs_options = {
    "qdr:h",  # 过去一小时内的结果
    "qdr:d",  # 过去一天内的结果
    "qdr:w",  # 过去一周内的结果
    "qdr:m",  # 过去一月内的结果
    "qdr:y"   # 过去一年内的结果
}
```

### 其他搜索参数

```python
params = {
    "hl": "zh-CN",     # 界面语言
    "lr": "lang_zh",   # 搜索结果语言
    "safe": "active",  # 安全搜索设置
    "start": 0,        # 结果起始位置（分页用）
    "num": 100,        # 返回结果数量（最大100）
}
```

### 高级搜索示例

```python
# 在特定网站中搜索PDF文件
term = "site:example.com filetype:pdf Python 编程"

# 搜索特定时间范围内的新闻
term = "人工智能 site:cnn.com"
tbs = "qdr:d"  # 过去24小时内的结果

# 精确匹配标题中的短语
term = 'intitle:"机器学习" site:arxiv.org'

# 排除特定内容
term = "Python 编程 -初学者 -教程 site:github.com"
```

## 配置管理

### 代理配置

1. **不使用代理**
   - 直接删除或注释掉 proxy 参数
   - 确保搜索函数中的 proxy 参数也被注释掉

2. **使用代理**
   - 取消注释 proxy 配置
   - 修改代理地址为您的实际代理服务器地址

### 打包说明

使用 PyInstaller 打包时，需要确保配置文件被正确包含：

```python
# your_script.spec
a = Analysis(
    ['your_script.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('googlesearch/config/data/all_domain.txt', 'googlesearch/config/data'),
        ('googlesearch/config/data/user_agents.txt', 'googlesearch/config/data'),
    ],
    # ... 其他配置 ...
)
```

## 常见问题

### 为什么我的请求总是超时？

请检查您的网络连接和代理设置。确保代理配置正确，目标网站没有被屏蔽。

### 如何进行更复杂的查询？

您可以使用 Google 搜索高级语法（如 `site:`、`filetype:` 等）来构建更复杂的查询字符串。

### 如何处理请求失败或异常？

请确保在您的请求中进行适当的异常处理，并查看错误日志以获取更多信息。您可以参考 [httpx 文档](https://www.python-httpx.org/) 了解更多异常处理信息。

## 参与贡献

我们非常欢迎社区成员参与项目建设！以下是几种参与方式：

### ⭐ 给项目点星

如果您觉得这个项目对您有帮助，欢迎点击右上角的 Star 按钮支持我们！

### 提交问题

发现了 Bug 或有新功能建议？欢迎提交 [Issue](https://github.com/huazz233/googlesearch/issues)！
- 🐛 Bug 反馈：请详细描述问题现象和复现步骤
- 💡 功能建议：请说明新功能的使用场景和预期效果

### Pull Request

想为项目贡献代码？非常欢迎提交 PR！

1. Fork 本仓库
2. 创建新分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 Pull Request

我们会认真审查每一个 PR，并提供及时反馈。

## 社区支持

- 📫 邮箱联系：[huazz233@163.com](mailto:huazz233@163.com)
- 💬 问题反馈：[GitHub Issues](https://github.com/huazz233/googlesearch/issues)
- 📖 开发文档：[Wiki](https://github.com/huazz233/googlesearch/wiki)
- 👥 讨论区：[Discussions](https://github.com/huazz233/googlesearch/discussions)

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

---

> 更多详细的 Google 搜索运算符和高级搜索技巧，请访问 [Google 搜索帮助](https://support.google.com/websearch/answer/2466433)。
