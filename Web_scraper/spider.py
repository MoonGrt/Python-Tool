from dis import findlinestarts
import re
from unicodedata import name
from urllib import response
import urllib.request
import urllib.error
import xlwt
from bs4 import BeautifulSoup
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "doubanmoive_250.xls"
    saveData(datalist,savepath)

findlink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #re.S使包括换行符
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askURL(url)

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):
            data = []
            item = str(item)
        
            link = re.findall(findlink,item)[0]
            data.append(link)

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            title = re.findall(findTitle,item)
            if len(title)==2:
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("/","")
                data.append(otitle)
            else:
                data.append(title[0])
                data.append(' ')

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)
            if len(inq)!=0:
                inq=inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd,item)[0]
            bd = re.sub(r'<br(\s+)?/>(\s+)'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())

            datalist.append(data)
    
    return datalist


def askURL(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    requset = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(requset)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    
    return html


def saveData(datalist,savepath):
    print("Save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('doubanmoive_250',cell_overwrite_ok=True)
    col = ("Moive","Link","Chinese","Freng","Mark","Num","Introduction","Relavant")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print(f"{i}")
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])

    book.save('doubanmoive_250.xls')


if __name__ == "__main__":
    main()
    print("Successful")
