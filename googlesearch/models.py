from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    搜索结果数据类
    Search result data class

    Attributes:
        url (str): 结果URL / Result URL
        title (str): 结果标题 / Result title
        description (str): 结果描述 / Result description
    """
    url: str
    title: str
    description: str

    def __post_init__(self):
        """清理字段空白 / Clean field whitespace"""
        self.url = self.url.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()

    def to_dict(self):
        """转换为字典 / Convert to dictionary"""
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
        }

    def __str__(self):
        return f"SearchResult(title='{self.title}', url='{self.url}')"
