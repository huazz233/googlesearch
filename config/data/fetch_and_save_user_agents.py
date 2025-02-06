#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Description: 获取并保存最新的 Chrome User-Agent
@Author: huazz
"""
import requests
from bs4 import BeautifulSoup
import sys


def fetch_useragents(url):
    """
    从指定 URL 获取 User-Agent 列表
    Fetch User-Agent list from specified URL

    Args:
        url (str): 目标网页 URL / Target webpage URL

    Returns:
        list: User-Agent 字符串列表 / List of User-Agent strings
    """
    try:
        # 发送 HTTP GET 请求获取网页内容 / Send HTTP GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析网页内容 / Parse webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有 User-Agent 字符串 / Find all User-Agent strings
        useragent_values = []
        
        # 解析 whatmyuseragent.com 的数据 / Parse data from whatmyuseragent.com
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3 and cols[2].get_text(strip=True) == 'desktop':
                useragent_values.append(cols[0].get_text(strip=True))

        return useragent_values
    except Exception as e:
        print(f"Error fetching User-Agents from {url}: {str(e)}")
        return []


def save_useragents_to_file(useragents, file_path):
    """
    将 User-Agent 列表保存到文件
    Save User-Agent list to file

    Args:
        useragents (list): User-Agent 列表 / List of User-Agents
        file_path (str): 保存文件路径 / Save file path

    Returns:
        bool: 是否保存成功 / Whether save successful
    """
    try:
        # 去重并保持顺序 / Remove duplicates while preserving order
        unique_useragents = list(dict.fromkeys(useragents))
        
        # 将 User-Agent 写入文件 / Write User-Agents to file
        with open(file_path, 'w', encoding='utf-8') as file:
            for useragent in unique_useragents:
                file.write(f"{useragent}\n")

        print(f"User-Agents saved successfully to {file_path}")
        print(f"Total unique User-Agents: {len(set(unique_useragents))}")
        return True
    except Exception as e:
        print(f"Error saving User-Agents to file: {str(e)}")
        return False


def main():
    """
    获取并保存 User-Agent 的主函数
    Main function to fetch and save User-Agents

    Returns:
        bool: 是否执行成功 / Whether execution successful
    """
    # 指定 User-Agent 来源 / User-Agent sources
    urls = [
        'https://whatmyuseragent.com/browser/ch/chrome/',
        'https://whatmyuseragent.com/browser/ch/chrome/127'
    ]
    
    file_path = 'user_agents.txt'
    all_useragents = []

    # 从所有来源获取 / Fetch from all sources
    for url in urls:
        useragents = fetch_useragents(url)
        all_useragents.extend(useragents)

    if not all_useragents:
        print("No User-Agents were fetched")
        return False

    return save_useragents_to_file(all_useragents, file_path)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
