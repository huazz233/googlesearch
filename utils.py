import re
from typing import List

from googlesearch.models import SearchResult


def deduplicate(results: List[SearchResult]) -> List[SearchResult]:
    """去重搜索结果"""
    seen = set()
    deduped_results = []
    for result in results:
        key = (result.url, result.title)
        if key not in seen:
            seen.add(key)
            deduped_results.append(result)
    return deduped_results

def clean_description(description: str) -> str:
    """清理描述文本"""
    # 移除多余空白
    description = ' '.join(description.split())
    # 移除时间戳部分
    description = re.sub(r'\d+ \w+ ago — \.\.\.', '', description)
    return description.strip()

def format_search_term(term: str, site: str = None) -> str:
    """格式化搜索词"""
    term = term.strip()
    if site:
        term = f"{term} site:{site}"
    return term.replace(' site:', '+site:')

def parse_time_string(time_str: str) -> str:
    """统一时间字符串格式"""
    if not time_str or time_str == "未知时间":
        return None
    return time_str.strip()
