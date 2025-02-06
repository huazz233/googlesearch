from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def fetch_domains(url):
    """
    Fetch Google domain list from specified URL
    从指定URL获取Google域名列表

    Args:
        url (str): Target webpage URL / 目标网页URL

    Returns:
        list: List of domains / 域名列表
    """
    try:
        # Send HTTP GET request to get webpage content / 发送HTTP GET请求获取网页内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse webpage content using BeautifulSoup / 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        domains = set()
        
        # Different parsing logic for different sources / 针对不同来源使用不同的解析逻辑
        if 'fobnotes.com' in url:
            # Find all <a> tags and extract domains / 查找所有<a>标签并提取域名
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                domain = urlparse(href).netloc
                if 'google' in domain.lower():
                    domains.add(domain)
        elif 'google.com' in url:
            # Extract domains from Google's country selector / 从Google的国家选择器中提取域名
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
    Save domain list to file
    将域名列表保存到文件

    Args:
        domains (list): List of domains / 域名列表
        file_path (str): Save file path / 保存文件路径
    """
    try:
        # Remove duplicates and sort / 去重并排序
        unique_domains = sorted(set(domains))
        
        # Write domains to file / 将域名写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            for domain in unique_domains:
                if domain:  # Only write non-empty domains / 只写入非空域名
                    file.write(f"{domain}\n")
        return True
    except Exception as e:
        print(f"Error saving domains to file: {str(e)}")
        return False


def main():
    """
    Main function to fetch and save Google domains
    获取并保存Google域名的主函数
    """
    # Multiple sources for Google domains / 多个Google域名来源
    urls = [
        'https://www.fobnotes.com/tools/google-global-country-sites/',
        'https://www.google.com/preferences?hl=en&fg=1'
    ]
    
    file_path = 'all_domain.txt'
    all_domains = []

    # Fetch from all sources / 从所有来源获取
    for url in urls:
        domains = fetch_domains(url)
        all_domains.extend(domains)

    # Add some known Google domains / 添加一些已知的Google域名
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

    if all_domains:
        if save_domains_to_file(all_domains, file_path):
            print(f"Domains saved successfully to {file_path}")
            print(f"Total unique domains: {len(set(all_domains))}")
        else:
            print("Failed to save domains")
    else:
        print("No domains were fetched")


if __name__ == "__main__":
    main()
