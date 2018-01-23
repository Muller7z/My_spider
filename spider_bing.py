
from lxml import html
import requests
import os

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


def spider(pag_num):
    pag_num += 1
    url = 'https://bing.ioliu.cn/?p=%s' % pag_num  # 构建主页面的url
    rsp = requests.get(url,headers=headers).content
    elm = html.fromstring(rsp)
    pag_url_list = elm.xpath('//a[@class="mark"]/@href')  # xpath解析出此页面下的图片的href地址
    img_url_finder(pag_url_list, pag_num)  # 调用下一级函数


def img_url_finder(url_list, pag):
    for each in url_list:
        url = "https://bing.ioliu.cn"+str(each)  # 构建url
        print("来自：%s"%url)
        rsp = requests.get(url,headers=headers).content
        elm = html.fromstring(rsp)
        down_url = "https://bing.ioliu.cn"+str(elm.xpath('//a[@class="ctrl download"]/@href')[0])  # 这是图片的下载地址
        img_title = str(elm.xpath('//p[@class="title"]/text()')[0])  # 这是图片的title
        #print(img_title)
        try :
            downloader(down_url, img_title)  # 这就是调用下载器了
        except Exception as e:
            print(e)
    print("完成下载第%s页" % str(pag))


def downloader(url,img_title):
    content = requests.get(url,timeout=5, headers=headers,).content
    i = img_title.index('(')
    # 图片的title含有特殊字符，会发生io错误，所以直接把后面的版权部分切掉了.......
    format_title = img_title[:i-1]+'.jpg'  # 这就是将要保存的文件名了
    with open(format_title,"wb")as f:
        f.write(content)
    print("正在下载壁纸:%s"%format_title)
    print("----------------------------------------------------------")


if __name__ == "__main__":

    dir_name = "wallpaper_from_bing"
    os.mkdir(dir_name)
    os.chdir(".\\%s"%dir_name)
    pag_number = input("请输入一个页数，将会从头开始下载壁纸至此页--->")
    for i in range(int(pag_number)):
        spider(i)
