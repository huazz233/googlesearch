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
