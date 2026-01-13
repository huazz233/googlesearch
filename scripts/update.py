#!/usr/bin/env python3
"""
更新 Google 域名列表
Update Google domain list

Usage: python scripts/update.py
"""
import os
import sys
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

# 数据文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_ROOT, "googlesearch", "resources", "all_domain.txt")

# 域名来源
SOURCES = [
    'https://www.fobnotes.com/tools/google-global-country-sites/',
    'https://www.google.com/preferences?hl=en&fg=1'
]

# 已知域名
KNOWN_DOMAINS = [
    'www.google.com', 'www.google.co.uk', 'www.google.de',
    'www.google.fr', 'www.google.co.jp', 'www.google.com.au', 'www.google.ca'
]


def fetch_domains(url):
    """从 URL 获取域名列表"""
    try:
        resp = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        domains = set()

        if 'fobnotes.com' in url:
            for a in soup.find_all('a', href=True):
                domain = urlparse(a['href']).netloc
                if 'google' in domain.lower():
                    domains.add(domain)
        elif 'google.com' in url:
            for opt in soup.find_all('option'):
                val = opt.get('value', '')
                if 'url=' in val:
                    parts = val.split('url=')[1].split('/')
                    if len(parts) > 2:
                        domains.add(parts[2])

        return list(domains)
    except Exception as e:
        print(f"Error: {url} - {e}")
        return []


def main():
    print("Fetching domains...")
    all_domains = KNOWN_DOMAINS.copy()

    for url in SOURCES:
        all_domains.extend(fetch_domains(url))

    unique = sorted(set(d for d in all_domains if d))

    if not unique:
        print("No domains found")
        return False

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique))

    print(f"Saved {len(unique)} domains to {DATA_FILE}")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
