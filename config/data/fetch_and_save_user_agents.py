import requests
from bs4 import BeautifulSoup


def fetch_useragents(url):
    # 发送HTTP GET请求获取网页内容
    response = requests.get(url)
    # 确保请求成功
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return []

    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有<tr>元素
    rows = soup.find_all('tr')

    # 筛选出符合条件的 User-Agent
    useragent_values = []
    for row in rows:
        # 查找所有<td>元素
        cols = row.find_all('td')
        # 确保<td>元素的数量足够
        if len(cols) >= 3 and cols[2].get_text(strip=True) == 'desktop':
            useragent_values.append(cols[0].get_text(strip=True))

    return useragent_values


def save_useragents_to_file(useragents, file_path):
    # 将标题和 User-Agent 写入文件
    with open(file_path, 'w') as file:
        for useragent in useragents:
            file.write(f"{useragent}\n")


url = 'https://whatmyuseragent.com/browser/ch/chrome/'
url_2 = 'https://whatmyuseragent.com/browser/ch/chrome/127'
file_path = 'user_agents.txt'

# 调用函数并保存结果到文件
useragents = fetch_useragents(url)
useragents += fetch_useragents(url_2)
if useragents:
    save_useragents_to_file(useragents, file_path)
    print(f"过滤后的 User-Agent 已保存到 {file_path}")
else:
    print("未能提取 User-Agent")
