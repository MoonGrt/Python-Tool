import lxml.etree, requests, os

if not os.path.exists('./picLabs'):
    os.mkdir('./picLabs')

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

for num in range(1,11):
    tree = lxml.etree.HTML(requests.get(f'https://pic.netbian.com/4k/index_{num}.html', headers=headers).text)
    li_list = tree.xpath('//div[@class="slist"]/ul/li')

    for li in li_list:
        img_src = 'https://pic.netbian.com' + li.xpath('./a/img/@src')[0]
        img_name = (li.xpath('./a/img/@alt')[0]+'.jpg').encode('iso-8859-1').decode('gbk')

        with open('picLabs/'+img_name, 'wb') as wfile:
            wfile.write(requests.get(url=img_src, headers=headers).content)
            print(img_name, 'Download')