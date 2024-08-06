import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def fetch_domains(url):
    # 发送 HTTP GET 请求获取网页内容
    response = requests.get(url)
    # 确保请求成功
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    # 使用 BeautifulSoup 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    domains = set()
    # 查找所有 <a> 标签
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        domain = urlparse(href).netloc
        if domain:
            domains.add(domain)

    return list(domains)


def save_domains_to_file(domains, file_path):
    # 将域名写入文件
    with open(file_path, 'w') as file:
        for domain in domains:
            file.write(f"{domain}\n")


if __name__ == "__main__":
    url = 'https://www.fobnotes.com/tools/google-global-country-sites/'
    file_path = 'domain.txt'

    # 调用函数并保存结果到文件
    domains = fetch_domains(url)
    if domains:
        save_domains_to_file(domains, file_path)
        print(f"域名已保存到 {file_path}")
    else:
        print("未能提取域名")
