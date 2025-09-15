from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchResult:
    """
    搜索结果数据类
    Search result data class
    
    Attributes:
        url (str): 结果URL / Result URL
        title (str): 结果标题 / Result title
        description (str): 结果描述 / Result description
        time (Optional[str]): 结果时间信息，可选 / Result time information, optional
    """
    url: str
    title: str
    description: str
    time: Optional[str] = None

    def __post_init__(self):
        """
        数据初始化后的处理
        Post-initialization processing
        
        清理所有字段的前后空白字符
        Cleans leading and trailing whitespace from all fields
        """
        self.url = self.url.strip()
        self.title = self.title.strip()
        self.description = self.description.strip()
        if self.time:
            self.time = self.time.strip()

    def to_dict(self):
        """
        将搜索结果转换为字典格式
        Convert search result to dictionary format
        
        Returns:
            dict: 包含所有字段的字典 / Dictionary containing all fields
                {
                    'url': str,
                    'title': str,
                    'description': str,
                    'time': Optional[str]
                }
        """
        return {
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'time': self.time
        }

    def __str__(self):
        """
        返回搜索结果的字符串表示
        Return string representation of search result
        
        Returns:
            str: 格式化的字符串，包含标题和URL
                 Formatted string containing title and URL
        """
        return f"SearchResult(title='{self.title}', url='{self.url}')"
