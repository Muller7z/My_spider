
from lxml import html
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


def spider(num):
    url = 'https://bing.ioliu.cn/?p=%s'%num
    rsp = requests.get(url,headers).content
    elm = html.fromstring(rsp)
    pag_url_list = elm.xpath('//a[@class="mark"]/@href')
    url_downloader(pag_url_list,num)


def url_downloader(list,num):
    for each in list:
        url = "https://bing.ioliu.cn"+str(each)
        rsp = requests.get(url,headers).content
        elm = html.fromstring(rsp)
        down_url = "https://bing.ioliu.cn"+str(elm.xpath('//a[@class="ctrl download"]/@href')[0])
        img_title = str(elm.xpath('//p[@class="title"]/text()')[0])
        try :
            downloader(down_url, img_title, num)
        except TypeError as e:
            print(e)
        except ValueError as v:
            print(v)
    print("完成下载第%s页"%num)


def downloader(url,img_title,num):
    content = requests.get(url,headers).content
    i = img_title.index('(')
    format_title = img_title[:i]+"_p%s"%num +'.jpg'
    with open(format_title,"wb")as f:
        f.write(content)
    print("正在下载壁纸——————%s"%format_title)
    print(url)


if __name__ == "__main__":
    for num in range(30,50):
        spider(num)

