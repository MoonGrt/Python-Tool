import requests, re, os, json, time
from tqdm import tqdm  #进度条模块

if not os.path.exists('./Video'):
    os.mkdir('./Video')

def down_from_url(url, dst):
    response = requests.get(url, stream=True)# 设置stream=True参数读取大文件
    # 通过header的content-length属性可以获取文件的总容量
    file_size = int(response.headers['content-length'])
    if os.path.exists(dst):
        # 获取本地已经下载的部分文件的容量，方便继续下载，如果不存在就从头开始下载。
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    # 如果大于或者等于则表示已经下载完成，否则继续
    if first_byte >= file_size:
        return file_size
    header = {"Range": f"bytes={first_byte}-{file_size}"}
 
    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True)
    with open(dst, 'ab') as f:
        # 每次读取一个1024个字节
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size
 
 
if __name__ == '__main__':
    url = "https://vdownload-1.hembed.com/39262-1080p.mp4?token=OFy7B_rRUMAtYTtHKR_8fg&expires=1663946364"
    # 根据时间戳生成文件名
    down_from_url(url,f"./Video/{time.time()}.mp4")

    