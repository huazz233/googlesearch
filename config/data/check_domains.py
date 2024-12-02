# -*- coding: utf-8 -*-
"""
@Project    : googlesearch
@File       : test.py
@Time       : 2024/12/2 09:27
@Author     : huazz
@Description: Description of test.py
@Version    : 1.0
"""
import platform
import subprocess
import time
from typing import List


def remove_duplicates(file_path: str) -> List[str]:
    """
    从文件中读取域名并去除重复项
    Read domains from file and remove duplicates

    Args:
        file_path (str): 域名文件路径 / Domain file path

    Returns:
        List[str]: 去重后的域名列表 / Deduplicated domain list
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            domains = f.read().splitlines()

        # 使用set去重，然后转回list并排序 / Use set for deduplication, then convert back to sorted list
        unique_domains = sorted(list(set(domains)))

        # 将去重结果写回文件 / Write deduplicated results back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_domains))

        print(f"去重完成 / Deduplication completed: 原有 / Original {len(domains)} 个域名，去重后剩余 / Remaining after deduplication {len(unique_domains)} 个域名")
        return unique_domains

    except Exception as e:
        print(f"去重过程出错 / Error during deduplication: {str(e)}")
        return []


def ping_domain(domain: str) -> bool:
    """
    检查域名是否可以ping通
    Check if domain is pingable

    Args:
        domain (str): 要检查的域名 / Domain to check

    Returns:
        bool: 是否可以ping通 / Whether pingable
    """
    # 移除域名开头的www. / Remove www. from domain beginning
    host = domain.replace('www.', '')

    try:
        # 根据操作系统选择ping命令 / Choose ping command based on OS
        if platform.system().lower() == "windows":
            command = ["ping", "-n", "1", "-w", "2000", host]
        else:
            command = ["ping", "-c", "1", "-W", "2", host]

        # 执行ping命令 / Execute ping command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    except Exception as e:
        print(f"Ping {domain} 失败 / failed: {str(e)}")
        return False


def check_domains(domains: List[str], output_file: str) -> List[str]:
    """
    检查域名列表的可用性
    Check availability of domain list

    Args:
        domains (List[str]): 要检查的域名列表 / List of domains to check
        output_file (str): 输出文件路径 / Output file path

    Returns:
        List[str]: 可用的域名列表 / List of available domains
    """
    working_domains = []
    total = len(domains)

    try:
        for i, domain in enumerate(domains, 1):
            is_working = ping_domain(domain)

            if is_working:
                working_domains.append(domain)
                print(f"[{i}/{total}] {domain} - 可访问 / accessible")
            else:
                print(f"[{i}/{total}] {domain} - 无法访问 / inaccessible")

            # 添加短暂延迟，避免请求过快
            time.sleep(0.5)

        # 将可用域名写入新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(working_domains))

        print(f"\n检查完成 / Check completed: 共 {total} 个域名，可用 / Available {len(working_domains)} 个")
        return working_domains

    except Exception as e:
        print(f"检查过程出错 / Error during check: {str(e)}")
        return []


def main():
    # 文件路径配置
    input_file = 'all_domain.txt'
    output_file = 'all_domain.txt'

    # 第一步：去重
    print("开始去重 / Starting deduplication...")
    unique_domains = remove_duplicates(input_file)

    if not unique_domains:
        print("去重失败，程序终止 / Deduplication failed, program terminated")
        return

    # 第二步：检查可用性
    print("\n开始检查域名可用性 / Starting check domain availability...")
    working_domains = check_domains(unique_domains, output_file)

    if not working_domains:
        print("域名检查失败，程序终止 / Domain check failed, program terminated")
        return

    print(f"\n处理完成！可用域名已保存至: {output_file}")


if __name__ == "__main__":
    main()
