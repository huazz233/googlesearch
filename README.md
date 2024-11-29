# GooglSearch-Tool

**GooglSearch-Tool** 是一个 Python 库，用于进行 Google 搜索并获取搜索结果。支持动态查询参数、结果去重以及自定义代理配置。

[![GitHub stars](https://img.shields.io/github/stars/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/issues)
[![GitHub license](https://img.shields.io/github/license/yourusername/googlesearch-tool.svg)](https://github.com/yourusername/googlesearch-tool/blob/master/LICENSE)

简体中文 | [English](README_EN.md)

## 目录

- [特性](#特性)
- [安装](#安装)
- [快速开始](#快速开始)
- [高级用法](#高级用法)
- [配置说明](#配置说明)
- [打包说明](#打包说明)
- [常见问题](#常见问题)
- [参与贡献](#参与贡献)
- [社区支持](#社区支持)

## 特性

- 支持 Google 搜索
- 可配置的查询参数（包括时间范围）
- 根据标题、URL 和摘要进行结果去重
- 支持自定义代理
- 搜索结果包括标题、链接、描述和时间信息
- 使用随机域名进行请求，防止访问受限
- 随机选择 User-Agent 请求头
- 手动更新并保存最新的 User-Agent 和 Google 域名列表（函数与保存位置在 `/config/data` 目录）

## 安装

可以通过 `pip` 安装 `googlesearch-tool`：

```bash
pip install googlesearch-tool
```

## 快速开始

以下是使用 GooglSearch-Tool 库的基本示例：

```python 
import asyncio
from googlesearch.config.config import Config
from googlesearch.search import search
from googlesearch.news_search import search_news

async def main():
    # 配置代理（可选）
    proxies = {
        "http://": "http://127.0.0.1:10809",
        "https://": "http://127.0.0.1:10809"
    }

    # 获取随机域名和User-Agent
    url = Config.get_random_domain()
    headers = {"User-Agent": Config.get_random_user_agent()}
    
    # 普通搜索
    results = await search(
        url=url,
        headers=headers,
        term="python site:cnn.com",
        num=100,
        tbs="qdr:h",  # 过去一小时的结果
        proxies=proxies
    )
    
    # 打印搜索结果
    for result in results:
        print(f"标题: {result.title}")
        print(f"链接: {result.url}")
        print(f"摘要: {result.description}")
        print(f"时间: {result.time}\n")

    # 新闻搜索
    news_results = await search_news(
        url=url,
        headers=headers,
        term="python site:cnn.com",
        num=100,
        tbs="qdr:d",  # 过去一天的结果
        proxy=proxies
    )
    
    # 打印新闻搜索结果
    for result in news_results:
        print(f"标题: {result.title}")
        print(f"链接: {result.url}")
        print(f"摘要: {result.description}")
        print(f"时间: {result.time}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### 参数说明

- `url`: 通过 `Config.get_random_domain()` 获取的随机 Google 域名
- `headers`: 包含随机 User-Agent 的请求头
- `term`: 搜索查询字符串
- `num`: 要获取的结果数量
- `tbs`: 时间范围参数
  - `qdr:h` - 过去一小时
  - `qdr:d` - 过去一天
  - `qdr:w` - 过去一周
  - `qdr:m` - 过去一月
  - `qdr:y` - 过去一年
- `proxies`: 代理配置（可选）
- `timeout`: 请求超时时间（秒）

### 结果对象

每个搜索结果的对象包含以下字段：

- `link`：结果的 URL
- `title`：结果的标题
- `description`：结果的描述
- `time_string`：结果的时间信息（如果有）

## 高级用法

### 获取随机域名和请求头

为了避免请求被限制，库提供了获取随机 Google 搜索域名和随机 User-Agent 的功能：

```python 
from googlesearch.config.config import Config

# 获取随机 Google 搜索域名
url = Config.get_random_domain()
print(url)  # 输出示例: https://www.google.ge/search

# 获取随机 User-Agent
headers = {"User-Agent": Config.get_random_user_agent()}
print(headers)  # 输出示例: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.1.7760.206 Safari/537.36'}
```

### 域名和 User-Agent 更新

域名列表和 User-Agent 列表存储在 `config/data` 目录下：
- `all_domain.txt`: 包含所有可用的 Google 搜索域名
- `user_agents.txt`: 包含最新的 Chrome User-Agent 列表

如需更新这些列表：
1. 运行 `fetch_and_save_user_domain.py` 更新域名列表
2. 运行 `fetch_and_save_user_agents.py` 更新 User-Agent 列表

## 配置说明

### 为什么我的请求总是超时？

请检查您的网络连接和代理设置。确保代理配置正确，并且目标网站没有被屏蔽。

### 如何进行更复杂的查询？

您可以使用 Google 搜索的高级语法（如 `site:`、`filetype:` 等）来构造更复杂的查询字符串。

### 如何处理请求失败或异常？

请确保在请求中设置适当的异常处理，并查看错误日志以获取更多信息。可以参考 [httpx 文档](https://www.python-httpx.org/) 了解更多关于异常处理的信息。

## 打包说明

使用 PyInstaller 打包时，需要确保配置文件被正确包含。以下是打包步骤和注意事项：

### 1. 创建 spec 文件

```bash
pyi-makespec --onefile your_script.py
```

### 2. 修改 spec 文件

需要在 spec 文件中添加 datas 参数，确保包含必要的配置文件：

```python 
# your_script.spec
a = Analysis(
    ['your_script.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 添加配置文件
        ('googlesearch/config/data/all_domain.txt', 'googlesearch/config/data'),
        ('googlesearch/config/data/user_agents.txt', 'googlesearch/config/data'),
    ],
    # ... 其他配置 ...
)
```

### 3. 使用 spec 文件打包

```bash
pyinstaller your_script.spec
```

### 4. 验证打包结果

运行打包后的程序，确保能正确读取配置文件：
```python 
from googlesearch.config.config import Config

# 测试配置文件是否正确加载
url = Config.get_random_domain()
headers = {"User-Agent": Config.get_random_user_agent()}
```

如果出现文件未找到的错误，请检查 spec 文件中的路径配置是否正确。

## 常见问题

### 为什么我的请求总是超时？

请检查您的网络连接和代理设置。确保代理配置正确，并且目标网站没有被屏蔽。

### 如何进行更复杂的查询？

您可以使用 Google 搜索的高级语法（如 `site:` 等）来构造更复杂的查询字符串。

### 如何处理请求失败或异常？

请确保在请求中设置适当的异常处理，并查看错误日志以获取更多信息。可以参考 [httpx 文档](https://www.python-httpx.org/) 了解更多关于异常处理的信息。

## 参与贡献

我们非常欢迎社区成员参与项目建设！以下是几种参与方式：

### Star ⭐ 本项目
如果您觉得这个项目对您有帮助，欢迎点击右上角的 Star 按钮支持我们！

### 提交 Issue 
发现 bug 或有新功能建议？欢迎提交 [Issue](https://github.com/yourusername/googlesearch-tool/issues)！
- 🐛 Bug 反馈：请详细描述问题现象和复现步骤
- 💡 功能建议：请说明新功能的使用场景和预期效果

### Pull Request
想要为项目贡献代码？非常欢迎提交 PR！

1. Fork 本仓库
2. 创建新分支: `git checkout -b feature/your-feature-name`
3. 提交更改: `git commit -am 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature-name`
5. 提交 Pull Request

我们会认真审查每一个 PR，并提供及时反馈。

## 社区支持

- 📫 邮件联系：[huazz233@163.com](mailto:huazz233@163.com)
- 💬 问题反馈：[GitHub Issues](https://github.com/yourusername/googlesearch-tool/issues)
- 📖 开发文档：[Wiki](https://github.com/yourusername/googlesearch-tool/wiki)
- 👥 讨论区：[Discussions](https://github.com/yourusername/googlesearch-tool/discussions)

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 了解详情
