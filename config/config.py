import os
import random


class Config:
    """全局配置"""

    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    UA_PATH = os.path.join(DATA_DIR, "user_agents.txt")
    DOMAIN_PATH = os.path.join(DATA_DIR, "all_domain.txt")

    @staticmethod
    def get_data(file_path):
        """从文件中读取数据并以列表格式输出

        Args:
            file_path (str): 文件路径
        """
        text_list = []
        with open(file_path, encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()  # 使用 strip() 来去除行首和行尾的空白字符，包括换行符
                if line:  # 只添加非空行
                    text_list.append(line)
        return text_list

    @staticmethod
    def load_user_agents():
        """加载 User-Agent 配置"""
        return Config.get_data(Config.UA_PATH)

    @staticmethod
    def load_domains():
        """加载搜索域名配置"""
        return Config.get_data(Config.DOMAIN_PATH)


    @staticmethod
    def get_random_user_agent():
        """从 User-Agent 列表中随机选择一个"""
        user_agents = Config.load_user_agents()
        return random.choice(user_agents) if user_agents \
            else "Mozilla/5.0 (X11; CrOS x86_64 15823.60.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.225 Safari/537.36"

    @staticmethod
    def get_random_domain():
        """从域名列表中随机选择一个域名"""
        domains = Config.load_domains()
        return random.choice(domains) if domains else "www.google.com"


# 从配置类中加载 User-Agent 和基本 URL
user_agent = Config.get_random_user_agent()
random_domain = Config.get_random_domain()
base_url = f"https://{random_domain}/search"
