import requests
from bs4 import BeautifulSoup


def fetch_useragents(url):
    """
    Fetch User-Agent list from specified URL
    从指定URL获取User-Agent列表

    Args:
        url (str): Target webpage URL / 目标网页URL

    Returns:
        list: List of User-Agent strings / User-Agent字符串列表
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

        # Find all User-Agent strings / 查找所有User-Agent字符串
        useragent_values = []
        
        # Different parsing logic for different sources / 针对不同来源使用不同的解析逻辑
        if 'useragents.me' in url:
            for item in soup.find_all('div', class_='useragent'):
                ua = item.get_text(strip=True)
                if 'Chrome' in ua and 'Mobile' not in ua:
                    useragent_values.append(ua)
        elif 'whatmyuseragent.com' in url:
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
    Save User-Agent list to file
    将User-Agent列表保存到文件

    Args:
        useragents (list): List of User-Agents / User-Agent列表
        file_path (str): Save file path / 保存文件路径
    """
    try:
        # Remove duplicates while preserving order / 去重并保持顺序
        unique_useragents = list(dict.fromkeys(useragents))
        
        # Write User-Agents to file / 将User-Agent写入文件
        with open(file_path, 'w', encoding='utf-8') as file:
            for useragent in unique_useragents:
                file.write(f"{useragent}\n")
        return True
    except Exception as e:
        print(f"Error saving User-Agents to file: {str(e)}")
        return False


def main():
    """
    Main function to fetch and save User-Agents
    获取并保存User-Agent的主函数
    """
    # Multiple sources for User-Agents / 多个User-Agent来源
    urls = [
        'https://www.useragents.me/chrome',
        'https://whatmyuseragent.com/browser/ch/chrome/',
        'https://whatmyuseragent.com/browser/ch/chrome/127'
    ]
    
    file_path = 'user_agents.txt'
    all_useragents = []

    # Fetch from all sources / 从所有来源获取
    for url in urls:
        useragents = fetch_useragents(url)
        all_useragents.extend(useragents)

    if all_useragents:
        if save_useragents_to_file(all_useragents, file_path):
            print(f"User-Agents saved successfully to {file_path}")
            print(f"Total unique User-Agents: {len(set(all_useragents))}")
        else:
            print("Failed to save User-Agents")
    else:
        print("No User-Agents were fetched")


if __name__ == "__main__":
    main()
