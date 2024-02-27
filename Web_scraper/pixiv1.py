import requests, re, os

if not os.path.exists('./Pic'):
    os.mkdir('./Pic')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "referer": "https://www.pixiv.net/"
}

num = 94615355
url = f"https://www.pixiv.net/artworks/{num}"
html = requests.get(url, headers=headers)
name = re.search('"illustTitle":"(.+?)"', html.text)                # 提取图片名称
picture = re.search('"original":"(.+?)"},"tags"', html.text)        # 提取图片原图地址
pic = requests.get(picture.group(1), headers=headers)
with open(f"./Pic/{name.group(1)}_{num}.{picture.group(1)[-3:]}", 'wb')as f:  # 创建一个以图片链接对应名字的文件
    f.write(pic.content)  # 将图片二进制数据存入，图片也就得到了
print(str(name.group(1)) + '_' + str(num) + ":下载成功")