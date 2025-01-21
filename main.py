#!/usr/bin/env python3
# coding=utf-8
# @Author: IceXaga <icexaga@outlook.com>

from bs4 import BeautifulSoup
import requests
red = '\033[31m'
green = '\033[92m'
yellow = '\033[93m'
reset = '\033[0m'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_title_up_name_pic(bvid):
    try:
        r = requests.get(f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}', headers=headers)
        r.raise_for_status()
        data = r.json()['data']
        title = data['title']
        title = title.replace("/", "").replace("\\", "").replace("?", "").replace("*", "").replace(":", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "")
        up = data['owner']['name']
        pic = data['pic']
        return title, up, pic
    except requests.exceptions.RequestException as e:
        print(f"{red}请求错误: {e}{reset}")
        return None, None
    except KeyError as e:
        print(f"{red}JSON解析错误: 缺少键 {e}{reset}")
        return None, None
    except Exception as e:
        print(f"{red}未知错误: {e}{reset}")
        return None, None

def get_tags_info(bvid):
    try:
        r = requests.get(f'https://www.bilibili.com/video/{bvid}', headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        tags = soup.find_all(class_='tag-link')
        info_elements = soup.find_all(class_='desc-info-text')
        info_text = ' '.join(element.get_text(strip=True) for element in info_elements)
        tagList = [tag.text.strip() for tag in tags]
        return tagList, info_text
    except requests.exceptions.RequestException as e:
        print(f"{red}请求错误: {e}{reset}")
        return [], "", ""
    except Exception as e:
        print(f"{red}未知错误: {e}{reset}")
        return [], "", ""

def write_to_file(bvid, title, up, tagList, info_text,pic):
    try:
        with open(f'{title}.md', mode="w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"title: {title}\n")
            f.write(f"up: {up}\n")
            f.write("tags:\n")
            for tag in tagList:
                f.write(f"  - {tag}\n")
            f.write("---\n\n")
            f.write(f"![{title}]({pic})\n\n")
            f.write(f"[{title}](https://www.bilibili.com/video/{bvid})\n\n")
            f.write(f"> [!简介]\n> {info_text}")
    except IOError as e:
        print(f"{red}文件写入错误: {e}{reset}")
if __name__ == '__main__':
    while True:
        bvid = str(input('请输入BV号> '))
        title, up, pic = get_title_up_name_pic(bvid)
        if not title or not up or not pic:
            continue
        tagList, info_text = get_tags_info(bvid)
        write_to_file(bvid, title, up, tagList, info_text,pic)
        print(f"{green}已成功生成{reset}{yellow}{title}.md{reset}")