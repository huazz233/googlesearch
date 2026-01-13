"""
配置管理 / Configuration management
"""
import os
import random

# 数据文件路径 / Data file path
_DATA_DIR = os.path.join(os.path.dirname(__file__), "resources")
_DOMAIN_PATH = os.path.join(_DATA_DIR, "all_domain.txt")

# 域名列表 / Domain list
_domains = ["www.google.com"]


def _load_domains():
    """加载域名列表 / Load domain list"""
    global _domains
    try:
        with open(_DOMAIN_PATH, encoding="utf-8") as f:
            domains = [line.strip() for line in f if line.strip()]
            if domains:
                _domains = domains
    except Exception:
        pass


def get_random_user_agent():
    """
    获取随机 Opera Mini User-Agent
    Get random Opera Mini User-Agent

    Opera Mini UA 可绕过 Google 的 JavaScript 检测
    Opera Mini UA bypasses Google's JavaScript detection

    参考 / Reference: https://github.com/deedy5/ddgs
    """
    patterns = [
        "Opera/9.80 (J2ME/MIDP; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (Android; Linux; Opera Mobi/{mb}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (iPhone; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
        "Opera/9.80 (iPad; Opera Mini/{v}/{b}; U; {l}) Presto/{p} Version/{f}",
    ]
    mini_versions = ["4.0", "5.0.17381", "7.1.32444", "9.80"]
    mobi_builds = ["27", "447", "ADR-1011151731"]
    builds = ["18.678", "24.743", "503"]
    prestos = ["2.6.35", "2.7.60", "2.8.119"]
    finals = ["10.00", "11.10", "12.16"]
    langs = ["en-US", "en-GB", "de-DE", "fr-FR", "es-ES", "ru-RU", "zh-CN"]

    pattern = random.choice(patterns)
    replacements = {
        "{l}": random.choice(langs),
        "{p}": random.choice(prestos),
        "{f}": random.choice(finals),
        "{v}": random.choice(mini_versions),
        "{b}": random.choice(builds),
        "{mb}": random.choice(mobi_builds),
    }

    result = pattern
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def get_random_domain():
    """获取随机 Google 域名 / Get random Google domain"""
    return f"https://{random.choice(_domains)}/search"


# 初始化 / Initialize
_load_domains()
