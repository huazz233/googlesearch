import re
from typing import List, Set

from googlesearch.models import SearchResult


def deduplicate(results: List[SearchResult]) -> List[SearchResult]:
    """
    对搜索结果进行去重
    Deduplicate search results
    
    Args:
        results (List[SearchResult]): 搜索结果列表 / List of search results
        
    Returns:
        List[SearchResult]: 去重后的搜索结果列表 / Deduplicated list of search results
    """
    seen_urls: Set[str] = set()
    unique_results: List[SearchResult] = []
    
    for result in results:
        if result.url not in seen_urls:
            seen_urls.add(result.url)
            unique_results.append(result)
    
    return unique_results


def clean_description(text: str) -> str:
    """
    清理描述文本中的多余空白字符
    Clean extra whitespace characters from description text
    
    Args:
        text (str): 原始描述文本 / Original description text
        
    Returns:
        str: 清理后的描述文本 / Cleaned description text
    """
    # 替换多个空白为单个空格
    # Replace multiple whitespace with single space
    cleaned = re.sub(r'\s+', ' ', text)
    # 移除首尾空白
    # Remove leading and trailing whitespace
    return cleaned.strip()

def format_search_term(term: str, site: str = None) -> str:
    """
    格式化搜索词
    Format search term

    Args:
        term (str): 搜索词 / Search term
        site (str, optional): 站点限制 / Site restriction

    Returns:
        str: 格式化后的搜索词 / Formatted search term
    """
    term = term.strip()
    if site:
        term = f"{term} site:{site}"
    return term.replace(' site:', '+site:')

def parse_time_string(time_str: str) -> str:
    """
    统一时间字符串格式
    Standardize time string format

    Args:
        time_str (str): 原始时间字符串 / Original time string

    Returns:
        str: 标准化的时间字符串,如果无效则返回None / Standardized time string, or None if invalid
    """
    if not time_str or time_str == "未知时间":
        return None
    return time_str.strip()
