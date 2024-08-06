def deduplicate(results):
    seen = set()
    deduped_results = []
    for result in results:
        key = (result.url, result.description)
        if key not in seen:
            seen.add(key)
            deduped_results.append(result)
    return deduped_results

def clean_description(description):
    time_parts = description.split("ago — ...", 1)
    if len(time_parts) > 1:
        return time_parts[1].strip()
    return description
