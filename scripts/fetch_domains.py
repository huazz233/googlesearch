#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取并保存 Google 搜索域名列表
Fetch and save Google search domain list
"""
import os
import sys
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

# 数据文件路径 / Data file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_ROOT, "googlesearch", "config", "data", "all_domain.txt")


def fetch_domains(url):
    """
    从指定 URL 获取 Google 域名列表
    Fetch Google domain list from specified URL
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = httpx.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        domains = set()

        if 'fobnotes.com' in url:
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                domain = urlparse(href).netloc
                if 'google' in domain.lower():
                    domains.add(domain)
        elif 'google.com' in url:
            for option in soup.find_all('option'):
                value = option.get('value', '')
                if value.startswith('country') and 'url=' in value:
                    domain = value.split('url=')[1].split('/')[2]
                    if domain:
                        domains.add(domain)

        return list(domains)
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return []


def save_domains(domains, file_path):
    """保存域名列表到文件 / Save domain list to file"""
    try:
        unique_domains = sorted(set(d for d in domains if d))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_domains))
        print(f"Saved {len(unique_domains)} domains to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False


def main():
    urls = [
        'https://www.fobnotes.com/tools/google-global-country-sites/',
        'https://www.google.com/preferences?hl=en&fg=1'
    ]

    all_domains = []
    for url in urls:
        all_domains.extend(fetch_domains(url))

    # 添加已知域名 / Add known domains
    all_domains.extend([
        'www.google.com', 'www.google.co.uk', 'www.google.de',
        'www.google.fr', 'www.google.co.jp', 'www.google.com.au', 'www.google.ca'
    ])

    if not all_domains:
        print("No domains fetched")
        return False

    return save_domains(all_domains, DATA_FILE)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
