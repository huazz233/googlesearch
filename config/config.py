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
    UA_PATH = os.path.join(DATA_DIR, "user_agents.txt")
    DOMAIN_PATH = os.path.join(DATA_DIR, "all_domain.txt")

    # 初始默认值（作为备选）/ Initial default values (as fallback)
    _domains = ["www.google.com"]
    _user_agents = [
        "Mozilla/5.0 (X11; CrOS x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]

    @staticmethod
    def get_data(file_path):
        """
        从文件中读取数据
        Read data from file

        Args:
            file_path (str): 文件路径 / File path

        Returns:
            list: 文件内容列表 / List of file contents
        """
        try:
            with open(file_path, encoding="utf-8") as fp:
                return [line.strip() for line in fp if line.strip()]
        except Exception:
            return []

    @classmethod
    def load_user_agents(cls):
        """
        加载 User-Agent 列表
        Load User-Agent list
        """
        agents = cls.get_data(cls.UA_PATH)
        if agents:
            cls._user_agents = agents

    @classmethod
    def load_domains(cls):
        """
        加载域名列表
        Load domain list
        """
        domains = cls.get_data(cls.DOMAIN_PATH)
        if domains:
            cls._domains = domains

    @classmethod
    def get_random_user_agent(cls):
        """
        获取随机 User-Agent
        Get random User-Agent

        Returns:
            str: 随机User-Agent字符串 / Random User-Agent string
        """
        return random.choice(cls._user_agents)

    @classmethod
    def get_random_domain(cls):
        """
        获取随机域名
        Get random domain

        Returns:
            str: 随机域名URL / Random domain URL
        """
        domain = random.choice(cls._domains)
        return f"https://{domain}/search"


# 初始化加载 / Initial loading
Config.load_user_agents()
Config.load_domains()
