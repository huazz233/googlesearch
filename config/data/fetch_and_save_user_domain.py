from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def fetch_domains(url):
    """
    从指定URL获取Google域名列表
    Fetch Google domain list from specified URL

    Args:
        url (str): 目标网页URL / Target webpage URL

    Returns:
        list: 域名列表 / List of domains
    """
    # 发送HTTP GET请求获取网页内容 / Send HTTP GET request to get webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"请求失败，状态码 / Request failed, status code: {response.status_code}")
        return []

    # 使用BeautifulSoup解析网页内容 / Parse webpage content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    domains = set()
    # 查找所有<a>标签并提取域名 / Find all <a> tags and extract domains
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        domain = urlparse(href).netloc
        if domain:
            domains.add(domain)

    return list(domains)


def save_domains_to_file(domains, file_path):
    """
    将域名列表保存到文件
    Save domain list to file

    Args:
        domains (list): 域名列表 / List of domains
        file_path (str): 保存文件路径 / Save file path
    """
    with open(file_path, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")


if __name__ == "__main__":
    # 目标URL和文件路径配置 / Target URL and file path configuration
    url = 'https://www.fobnotes.com/tools/google-global-country-sites/'
    file_path = 'all_domain.txt'

    # 调用函数并保存结果到文件
    domains = fetch_domains(url)
    if domains:
        save_domains_to_file(domains, file_path)
        print(f"域名已保存到 / Domains saved to: {file_path}")
    else:
        print("未能提取域名 / Failed to extract domains")
