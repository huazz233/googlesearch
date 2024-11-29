import os
import random


class Config:
    """配置管理"""

    # 基础路径配置
    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    UA_PATH = os.path.join(DATA_DIR, "user_agents.txt")
    DOMAIN_PATH = os.path.join(DATA_DIR, "all_domain.txt")

    # 初始默认值（作为备选）
    _domains = ["www.google.com"]
    _user_agents = [
        "Mozilla/5.0 (X11; CrOS x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ]

    @staticmethod
    def get_data(file_path):
        """从文件中读取数据"""
        try:
            with open(file_path, encoding="utf-8") as fp:
                return [line.strip() for line in fp if line.strip()]
        except Exception:
            return []

    @classmethod
    def load_user_agents(cls):
        """加载 User-Agent 列表"""
        agents = cls.get_data(cls.UA_PATH)
        if agents:
            cls._user_agents = agents

    @classmethod
    def load_domains(cls):
        """加载域名列表"""
        domains = cls.get_data(cls.DOMAIN_PATH)
        if domains:
            cls._domains = domains

    @classmethod
    def get_random_user_agent(cls):
        """获取随机 User-Agent"""
        return random.choice(cls._user_agents)

    @classmethod
    def get_random_domain(cls):
        """获取随机域名"""
        domain = random.choice(cls._domains)
        return f"https://{domain}/search"


# 初始化加载
Config.load_user_agents()
Config.load_domains()
