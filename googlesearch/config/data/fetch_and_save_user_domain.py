#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Description: 获取并保存 Google 搜索域名列表
@Author: huazz
"""
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
import sys


def fetch_domains(url):
    """
    从指定 URL 获取 Google 域名列表
    Fetch Google domain list from specified URL

    Args:
        url (str): 目标网页 URL / Target webpage URL

    Returns:
        list: 域名列表 / List of domains
    """
    try:
        # 发送 HTTP GET 请求获取网页内容 / Send HTTP GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析网页内容 / Parse webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        domains = set()
        
        # 针对不同来源使用不同的解析逻辑 / Different parsing logic for different sources
        if 'fobnotes.com' in url:
            # 查找所有<a>标签并提取域名 / Find all <a> tags and extract domains
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                domain = urlparse(href).netloc
                if 'google' in domain.lower():
                    domains.add(domain)
        elif 'google.com' in url:
            # 从 Google 的国家选择器中提取域名 / Extract domains from Google's country selector
            for option in soup.find_all('option'):
                value = option.get('value', '')
                if value.startswith('country') and 'url=' in value:
                    domain = value.split('url=')[1].split('/')[2]
                    if domain:
                        domains.add(domain)

        return list(domains)
    except Exception as e:
        print(f"Error fetching domains from {url}: {str(e)}")
        return []


def save_domains_to_file(domains, file_path):
    """
    将域名列表保存到文件
    Save domain list to file

    Args:
        domains (list): 域名列表 / List of domains
        file_path (str): 保存文件路径 / Save file path

    Returns:
        bool: 是否保存成功 / Whether save successful
    """
    try:
        # 去重并排序 / Remove duplicates and sort
        unique_domains = sorted(set(domains))
        
        # 将域名写入文件 / Write domains to file
        with open(file_path, 'w', encoding='utf-8') as file:
            for domain in unique_domains:
                if domain:  # 只写入非空域名 / Only write non-empty domains
                    file.write(f"{domain}\n")

        print(f"Domains saved successfully to {file_path}")
        print(f"Total unique domains: {len(unique_domains)}")
        return True
    except Exception as e:
        print(f"Error saving domains to file: {str(e)}")
        return False


def main():
    """
    获取并保存 Google 域名的主函数
    Main function to fetch and save Google domains

    Returns:
        bool: 是否执行成功 / Whether execution successful
    """
    # 指定域名来源 / Domain sources
    urls = [
        'https://www.fobnotes.com/tools/google-global-country-sites/',
        'https://www.google.com/preferences?hl=en&fg=1'
    ]
    
    file_path = 'all_domain.txt'
    all_domains = []

    # 从所有来源获取 / Fetch from all sources
    for url in urls:
        domains = fetch_domains(url)
        all_domains.extend(domains)

    # 添加一些已知的 Google 域名 / Add some known Google domains
    additional_domains = [
        'www.google.com',
        'www.google.co.uk',
        'www.google.de',
        'www.google.fr',
        'www.google.co.jp',
        'www.google.com.au',
        'www.google.ca'
    ]
    all_domains.extend(additional_domains)

    if not all_domains:
        print("No domains were fetched")
        return False

    return save_domains_to_file(all_domains, file_path)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
