import re
from typing import List

from googlesearch.models import SearchResult


def deduplicate(results: List[SearchResult]) -> List[SearchResult]:
    """
    去重搜索结果
    Deduplicate search results

    Args:
        results (List[SearchResult]): 搜索结果列表 / List of search results

    Returns:
        List[SearchResult]: 去重后的结果列表 / Deduplicated results list
    """
    seen = set()
    deduped_results = []
    for result in results:
        key = (result.url, result.title)
        if key not in seen:
            seen.add(key)
            deduped_results.append(result)
    return deduped_results

def clean_description(description: str) -> str:
    """
    清理描述文本
    Clean description text

    Args:
        description (str): 原始描述文本 / Original description text

    Returns:
        str: 清理后的描述文本 / Cleaned description text
    """
    # 移除多余空白 / Remove extra whitespace
    description = ' '.join(description.split())
    # 移除时间戳部分 / Remove timestamp part
    description = re.sub(r'\d+ \w+ ago — \.\.\.', '', description)
    return description.strip()

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
