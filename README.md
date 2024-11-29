# GooglSearch-Tool

**GooglSearch-Tool** 是一个 Python 库，用于进行 Google 搜索并获取搜索结果。支持动态查询参数、结果去重以及自定义代理配置。

[![GitHub stars](https://img.shields.io/github/stars/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/issues)
[![GitHub license](https://img.shields.io/github/license/huazz233/googlesearch.svg)](https://github.com/huazz233/googlesearch/blob/master/LICENSE)

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

### 基础示例

```python
import asyncio
from googlesearch.search import search
from googlesearch.news_search import search_news

async def test_search():
    """测试普通搜索"""
    try:
        """
        代理配置说明：
        1. 不使用代理：直接删除或注释掉 proxies 配置
        2. 使用代理：取消注释并修改代理地址
        """
        # 代理配置示例（如需使用，请取消注释并修改代理地址）
        # proxies = {
        #     "http://": "http://your-proxy-host:port",
        #     "https://": "http://your-proxy-host:port"
        # }
         
        print("\n=== 普通搜索结果 ===")
        results = await search(
            term="python programming",
            num=10,
            lang="en"
        )

        if not results:
            print("未找到搜索结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f"标题: {result.title}")
            print(f"链接: {result.url}")
            print(f"描述: {result.description}")
            if result.time:
                print(f"时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"普通搜索失败: {str(e)}")
        return False

async def test_news_search():
    """测试新闻搜索"""
    try:
        print("\n=== 新闻搜索结果 ===")
        results = await search_news(
            term="python news",
            num=5,
            lang="en"
        )

        if not results:
            print("未找到新闻结果")
            return False

        for i, result in enumerate(results, 1):
            print(f"\n新闻 {i}:")
            print(f"标题: {result.title}")
            print(f"链接: {result.url}")
            print(f"描述: {result.description}")
            if result.time:
                print(f"时间: {result.time}")
            print("-" * 80)

        return True
    except Exception as e:
        print(f"新闻搜索失败: {str(e)}")
        return False

async def main():
    """运行所有测试"""
    print("开始搜索...\n")
    await test_search()
    await test_news_search()

if __name__ == "__main__":
    asyncio.run(main())

```

### 代理配置说明

1. **不使用代理**
   - 直接删除或注释掉 proxies 配置
   - 确保搜索函数中的 proxies/proxy 参数也被注释掉

2. **使用代理**
   - 取消注释 proxies 配置
   - 修改代理地址为您的实际代理服务器地址
   - 取消注释搜索函数中的 proxies/proxy 参数

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

## 高级搜索语法

> 更多详细的 Google 搜索运算符和高级搜索技巧，请访问 [Google 搜索帮助](https://support.google.com/websearch/answer/2466433)。

### 基础搜索运算符

以下是一些常用的搜索运算符，使用时请注意运算符和搜索词之间不要有空格：

- **精确匹配搜索**：使用引号包围词组，如 `"exact phrase"`
- **站内搜索**：`site:domain.com keywords`
- **排除特定词**：使用减号排除词，如 `china -snake`
- **文件类型**：`filetype:pdf keywords`
- **标题搜索**：`intitle:keywords`
- **URL搜索**：`inurl:keywords`
- **多个条件**：`site:domain.com filetype:pdf keywords`

### 时间范围参数 (tbs)

搜索函数支持以下时间范围参数：

```python
tbs = {
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
    "hl": "zh-CN",     # 界面语言（例如：zh-CN, en）
    "lr": "lang_zh",   # 搜索结果语言
    "safe": "active",  # 安全搜索设置（"active"启用安全搜索）
    "start": 0,        # 结果起始位置（分页用）
    "num": 100,        # 返回结果数量（最大100）
}
```

### 高级搜索示例

```python
# 在特定网站中搜索PDF文件
term = "site:example.com filetype:pdf china programming"

# 搜索特定时间范围内的新闻
term = "china news site:cnn.com"
tbs = "qdr:d"  # 过去24小时内的结果

# 精确匹配标题中的短语
term = 'intitle:"machine learning" site:arxiv.org'

# 排除特定内容
term = "china programming -beginner -tutorial site:github.com"
```

### 搜索结果过滤

搜索结果可以按以下类型进行过滤：
- 网页（Web）
- 新闻（News）
- 图片（Images）
- 视频（Videos）

在我们的库中，已经为不同类型的搜索提供了专门的函数：
```python
# 普通网页搜索
results = await search(...)

# 新闻搜索
news_results = await search_news(...)
```

### 搜索技巧

1. **使用多个条件组合**
   ```python
   # 在多个特定网站中搜索
   term = "site:edu.cn OR site:ac.cn machine learning"
   ```

2. **使用通配符**
   ```python
   # 使用星号作为通配符
   term = "china * programming"
   ```

3. **使用数字范围**
   ```python
   # 搜索特定年份范围
   term = "china programming 2020..2024"
   ```

4. **相关词搜索**
   ```python
   # 使用波浪号搜索相关词
   term = "~programming tutorials"
   ```

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
发现 bug 或有新功能建议？欢迎提交 [Issue](https://github.com/huazz233/googlesearch/issues)！
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
- 💬 问题反馈：[GitHub Issues](https://github.com/huazz233/googlesearch/issues)
- 📖 开发文档：[Wiki](https://github.com/huazz233/googlesearch/wiki)
- 👥 讨论区：[Discussions](https://github.com/huazz233/googlesearch/discussions)

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 了解详情
