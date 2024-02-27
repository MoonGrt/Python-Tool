import requests, re, os, json, time

if not os.path.exists('./Pic'):
    os.mkdir('./Pic')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "referer": "https://www.mooyuu.com/"
}                                                                    

num = re.compile(r'<a href="/illust/(\d*)/"')
link = re.compile(r'<meta property="og:image" content="(.*?)" />')
name = re.compile(r'<title>(.*)mooyuu.com</title>')

url = "https://www.mooyuu.com/html/hot.html"
html = requests.get(url, headers=headers).text
ID = re.findall(num,html)
for id in ID:
    URL = f"https://www.mooyuu.com/illust/{id}/"
    item = requests.get(URL, headers=headers).text
    NAME = re.findall(name,item)
    LINK = re.findall(link,item)
    with open(f"./Pic/{NAME}" + LINK[0].split('/')[-1][-4:], 'wb') as f:             # 创建一个以图片链接对应名字的文件
        f.write(requests.get(url = LINK[0], headers=headers).content)                                     # 存入图片二进制数据
    print(NAME[0] + ": 下载成功")
    time.sleep(1)                                                     # 延迟一秒，防止ip被封