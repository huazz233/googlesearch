```markdown
# GooglSearch-Tool

**GooglSearch-Tool** 是一个 Python 库，用于进行 Google 搜索并获取搜索结果。支持动态查询参数、结果去重以及自定义代理配置。这个库主要用于 Web 数据抓取和分析。

## 特性

- 支持 Google 搜索
- 可配置的查询参数，包括时间范围
- 结果去重（根据标题、URL 和摘要）
- 支持自定义代理
- 结果包括标题、链接、描述和时间信息

## 安装

可以通过 `pip` 安装 `googlesearcher`：

```bash
pip install googlesearcher
```

## 使用方法

以下是使用 GooglSearch-Tool 库的基本示例：

```python
import asyncio
from googlesearch-tool import search

async def main():
    results = await search(
        term="xi site:www.theguardian.com",
        num=100,
        tbs="qdr:d",
        timeout=10,
        proxies={"http://": "http://your-proxy", "https://": "https://your-proxy"}
    )
    for result in results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 参数说明

- `term`：搜索查询字符串。
- `num`：要获取的结果数量。
- `tbs`：时间范围参数，如 `qdr:d` 表示过去一天。
- `timeout`：请求超时时间（秒）。
- `proxies`：自定义代理配置。

### 结果对象

每个搜索结果的对象包含以下字段：

- `link`：结果的 URL
- `title`：结果的标题
- `description`：结果的描述
- `time_string`：结果的时间信息（如果有）

## 常见问题

### 为什么我的请求总是超时？

请检查您的网络连接和代理设置。确保代理配置正确，并且目标网站没有被屏蔽。

### 如何进行更复杂的查询？

您可以使用 Google 搜索的高级语法（如 `site:`、`filetype:` 等）来构造更复杂的查询字符串。

### 如何处理请求失败或异常？

请确保在请求中设置适当的异常处理，并查看错误日志以获取更多信息。可以参考 [httpx 文档](https://www.python-httpx.org/) 了解更多关于异常处理的信息。

## 贡献

欢迎对项目进行贡献！请遵循以下步骤：

1. Fork 本项目
2. 创建新的分支 (`git checkout -b feature-branch`)
3. 提交更改 (`git commit -am 'Add new feature'`)
4. 推送到分支 (`git push origin feature-branch`)
5. 提交 Pull Request

## 许可证

本项目使用 [MIT 许可证](LICENSE)。

## 联系

如有任何问题或建议，请通过 [huazz233163.com](mailto:huazz233163.com) 与我们联系。
