from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchResult:
    """
    搜索结果数据类
    Search result data class
    
    Attributes:
        url (str): 结果链接 / Result URL
        title (str): 结果标题 / Result title
        description (str): 结果描述 / Result description
        time (Optional[str]): 结果时间（可选） / Result timestamp (optional)
    """
    url: str
    title: str
    description: str
    time: Optional[str] = None

    def __post_init__(self):
        """
        数据验证和清理
        Data validation and cleaning
        """
        self.url = self.url.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()
        if self.time:
            self.time = self.time.strip()

    def to_dict(self):
        """
        转换为字典格式
        Convert to dictionary format
        
        Returns:
            dict: 包含搜索结果所有字段的字典 / Dictionary containing all search result fields
        """
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'time': self.time
        }

    def __str__(self):
        """
        友好的字符串表示
        Friendly string representation
        
        Returns:
            str: 对象的字符串表示 / String representation of the object
        """
        return f"SearchResult(title='{self.title}', url='{self.url}')"
