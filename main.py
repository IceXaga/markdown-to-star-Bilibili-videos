from bs4 import BeautifulSoup
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
while True:
    bvid = str(input('请输入BV号> '))
    tagList = []
    data = requests.get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}', headers=headers).json()['data']
    soup = BeautifulSoup(requests.get(f'https://www.bilibili.com/video/{bvid}', headers=headers).content, 'html.parser')

    tags = soup.find_all(class_='tag-link')
    for tag in tags:
        tagList.append(tag.text.strip())
    
    info_elements = soup.find_all(class_='desc-info-text')
    info_text = ' '.join(element.get_text(strip=True) for element in info_elements)

    title = data['title']
    up = data['owner']['name']
    title = title.replace("/", "").replace("\\", "").replace("?", "").replace("*", "").replace(":", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "")
    with open(f'{title}.md', mode="w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: {title}\n")
        f.write(f"up: {up}\n")
        f.write("tags:\n")
        for tag in tagList:
            f.write(f"  - {tag}\n")
        f.write("---\n\n")
        f.write(f"[{title}](https://www.bilibili.com/video/{bvid})\n\n")
        f.write(f"> [!简介] {info_text}")