#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 Google 域名可用性
Check Google domain availability
"""
import os
import platform
import subprocess
import sys
import time
from typing import List

# 数据文件路径 / Data file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(PROJECT_ROOT, "googlesearch", "config", "data", "all_domain.txt")


def ping_domain(domain: str) -> bool:
    """检查域名是否可 ping / Check if domain is pingable"""
    host = domain.replace('www.', '')
    try:
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", "2000", host]
        else:
            cmd = ["ping", "-c", "1", "-W", "2", host]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"Ping {domain} failed: {e}")
        return False


def check_domains(domains: List[str]) -> List[str]:
    """检查域名列表可用性 / Check domain list availability"""
    working = []
    total = len(domains)

    for i, domain in enumerate(domains, 1):
        is_working = ping_domain(domain)
        status = "OK" if is_working else "FAIL"
        print(f"[{i}/{total}] {domain} - {status}")

        if is_working:
            working.append(domain)
        time.sleep(0.5)

    return working


def main():
    # 读取域名 / Read domains
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            domains = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading {DATA_FILE}: {e}")
        return False

    if not domains:
        print("No domains to check")
        return False

    # 去重 / Deduplicate
    unique = sorted(set(domains))
    print(f"Checking {len(unique)} unique domains...")

    # 检查 / Check
    working = check_domains(unique)

    # 保存可用域名 / Save working domains
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(working))
        print(f"\nDone: {len(working)}/{len(unique)} domains available")
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
