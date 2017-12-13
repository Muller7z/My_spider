
import requests
from lxml import html
import os


headers = {"Referer":"http://www.mzitu.com/","User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

dir_name = input("请输入文件夹的名字:  ")
os.mkdir(dir_name) # 新建一个一级目录
os.chdir("D:\Spider\%s"%dir_name)  # 进入一级目录
url_input = input("请输入链接地址：")


def taotu_url(url_target):
    '''获取分页的url'''
    try:
        rsp = requests.get(url_target,headers=headers).content
        elm = html.fromstring(rsp)
        page_number = elm.xpath('//a[@class="page-numbers"]/text()')[-1]
        print("此链接下有%s个页面待爬取" % page_number)
        for i in range(page_number):
            url = url_target+'page/%s/'%(i+1)
            print(url)
            response = requests.get(url,headers=headers).content
            elmt = html.fromstring(response)
            url_list = elmt.xpath('//ul[@id="pins"]/li/a/@href')  # 解析url 我使用的是xpath
            print(url_list)
            for each in url_list:
                #url_finder(each)
                print("正在查找分页")

    except Exception as e:
        with open("Error_logging.txt","wb")as f:
            error = str(e).encode(encoding="utf-8")
            f.write(error)  # 记录下错误日志
        print(e)


def url_finder(url):
    '''解析出套图中的图片数量、标题'''
    try:
        rsp = requests.get(url, headers=headers).content
        elm = html.fromstring(rsp)
        totle_nummber = str(elm.xpath('//div[@class="pagenavi"]//a/span/text()')[-2])
        file_title = str(elm.xpath('//div[@class="main"]//h2/text()')[0])
        print(file_title)
        downloader(url,totle_nummber,file_title)
    except Exception as e:
        with open("Error_logging.txt","wb")as f:
            error = str(e)+"联接超时,url="+ url
            f.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        print(e)


def downloader(url,nummber,title):
    '''构造分页的url，定位到下载url，并保存到本地'''
    try:
        os.mkdir("%s" % title)  # 新建一个二级目录
        os.chdir('D:\Spider\%s\%s' % (dir_name,title))  # 进入到二级目录
        for i in range(int(nummber)):
            url_real = url+"/" + str(i + 1)  # 根据图片总数 构造分页的url
            rsp = requests.get(url_real, headers=headers).content
            elm = html.fromstring(rsp)
            download_url = elm.xpath('//div[@class="main-image"]//img/@src')[0]  # 定位到下载url
            img_title = elm.xpath('//div[@class="content"]/h2/text()')[0] + '.jpg'
            print(str(img_title))
            with open(img_title, "wb")as f:
                f.write(requests.get(download_url, headers=headers).content)
                '''这里是请求下载url并且保存，返回的是防盗链警告图，referer该如何改才好呢？'''
        os.chdir('D:\Spider\%s'%dir_name)   # 切换回一级目录
    except Exception as e:
        with open("Error_logging.txt","wb")as f:
            error = str(e)+"联接超时,url="+ url
            f.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        print(e)


if __name__ == "__main__":
    taotu_url(url_input)

