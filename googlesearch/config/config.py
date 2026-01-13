import os
import random


class Config:
    """
    配置管理类
    Configuration management class
    """

    # 基础路径配置 / Base path configuration
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DOMAIN_PATH = os.path.join(DATA_DIR, "all_domain.txt")

    # 域名列表默认值 / Default domain list
    _domains = ["www.google.com"]

    @staticmethod
    def _load_file(file_path):
        """
        从文件中读取数据
        Read data from file
        """
        try:
            with open(file_path, encoding="utf-8") as fp:
                return [line.strip() for line in fp if line.strip()]
        except Exception:
            return []

    @classmethod
    def load_domains(cls):
        """
        加载域名列表
        Load domain list
        """
        domains = cls._load_file(cls.DOMAIN_PATH)
        if domains:
            cls._domains = domains

    @classmethod
    def get_random_user_agent(cls):
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

    @classmethod
    def get_random_domain(cls):
        """
        获取随机 Google 域名
        Get random Google domain
        """
        domain = random.choice(cls._domains)
        return f"https://{domain}/search"


# 初始化加载域名列表 / Load domain list on init
Config.load_domains()
