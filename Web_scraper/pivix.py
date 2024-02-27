import requests, re, os, json, time

if not os.path.exists('./Pic'):
    os.mkdir('./Pic')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    'cookie': 'first_visit_datetime_pc=2023-01-04+20:54:12; p_ab_id=6; p_ab_id_2=2; p_ab_d_id=676227908; yuid_b=EnV1ISg; PHPSESSID=83040790_2gXWQCAJxTyc7qGpxg8cjP99OGbmPHKy; device_token=ca18e92dcc0e278f9031e6b61adce30d; c_type=23; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=0; login_ever=yes; __cf_bm=yq6ZiQ9QX3fSFyysbSnp.0NxyCHFH.34QEj5VAhgvz4-1674828833-0-ARYwAzP2f38SApfvQ8Gep7M+K6JsYmlo2WxdktivYYAAJTfiY+8aaN6ygYsYymS9wvssK7cq+XvU6d81SMQWgvrZL8ZmHPr7tAeU7QfCa4WhjS7lrEKKj42fouwvk0mvImZdnxlD66GupSB3iDXiH57pPBAJe8bF6qPTY2/jrzlrdjXdeTYdlADGP/1pgnIlEs5RN1ELw3NIL+P7sl1lTNA=; p_b_type=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; tag_view_ranking=RcahSSzeRf~CrFcrMFJzz~-StjcwdYwv~LVSDGaCAdn~QKeXYK2oSR~qWFESUmfEs~Ie2c51_4Sp~CiSfl_AE0h~azESOjmQSV~Xyw8zvsyR4~Lt-oEicbBr~5oPIfUbtd6~tgP8r-gOe_~7WfWkHyQ76~JQVPs-pJr7~MV0x7YB32h~D0nMcn6oGk~jk9IzfjZ6n~KOnmT1ndWG~QaiOjmwQnI~-mS39rlV30~mzJgaDwBF5~LnLOEMuLbh~sylWziJEvL~CdwexeFTM2~aKhT3n4RHZ~a4NwQM4c8N~ePN3h1AXKX~QL2G1t5h_V',
    "referer": "https://www.pixiv.net/"
}                                                                    # p站的图片链接都是防盗链,加上 referer 才正常访问了

num = 104272976
url = f"https://www.pixiv.net/artworks/{num}"
name = re.search('"illustTitle":"(.+?)"', requests.get(url, headers=headers).text)              # 提取图片名称
url = f"https://www.pixiv.net/ajax/illust/{num}/pages"
res_json = requests.get(url, headers=headers).text
url_list = json.loads(res_json)['body']                               # 获得的数据先文本化，再用json.loads转化为字典数据
for i in url_list:                                                    # 依次输出urls对应数据下original对应的数据
    URL = i['urls']['original']
    Num = URL.split("/")[-1]                                          # 将图片链接以斜杠分割后取最后面的信息作为名字
    with open(f"./Pic/{name.group(1)}_{Num}", 'wb') as f:             # 创建一个以图片链接对应名字的文件
        f.write(requests.get(URL, headers=headers).content)                                     # 存入图片二进制数据
    print(f"{name.group(1)}_{Num}" + ": 下载成功")
    time.sleep(1)                                                     # 延迟一秒，防止ip被封