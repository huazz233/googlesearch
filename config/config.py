import os
import random


class Config:
    """全局配置"""

    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    UA_PATH = os.path.join(DATA_DIR, "user_agents.txt")
    DOMAIN_PATH = os.path.join(DATA_DIR, "all_domain.txt")

    # 初次加载域名列表和User-Agent列表
    all_domains = ["www.google.com"]  # 默认值，以防文件读取失败
    all_user_agents = [
        "Mozilla/5.0 (X11; CrOS x86_64 15823.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.225 Safari/537.36"]  # 默认值

    @staticmethod
    def get_data(file_path):
        """从文件中读取数据并以列表格式输出"""
        text_list = []
        with open(file_path, encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()  # 使用 strip() 来去除行首和行尾的空白字符，包括换行符
                if line:  # 只添加非空行
                    text_list.append(line)
        return text_list

    @classmethod
    def load_user_agents(cls):
        """加载 User-Agent 配置，仅在初次加载时调用"""
        cls.all_user_agents = cls.get_data(cls.UA_PATH)

    @classmethod
    def load_domains(cls):
        """加载搜索域名配置，仅在初次加载时调用"""
        cls.all_domains = cls.get_data(cls.DOMAIN_PATH)

    @classmethod
    def get_random_user_agent(cls):
        """从 User-Agent 列表中随机选择一个"""
        return random.choice(
            cls.all_user_agents) if cls.all_user_agents else "Mozilla/5.0 (X11; CrOS x86_64 15823.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.225 Safari/537.36"

    @classmethod
    def get_random_domain(cls):
        """从域名列表中随机选择一个域名"""
        random_domain = random.choice(cls.all_domains) if cls.all_domains else "www.google.com"
        return f"https://{random_domain}/search"


# 加载配置数据
Config.load_user_agents()
Config.load_domains()
