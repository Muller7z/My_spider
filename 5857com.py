
import requests
from lxml import html
import os

headers = {"Referer":"http://www.5857.com/sjbz/","User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}


def pag_finder(url):
    r = requests.get(url,headers=headers).content
    e = html.fromstring(r)
    page_href = e.xpath('//div[@class="page"]/a/@href')[:-1]
    pic_page_link = []
    if page_href == []:
        r = requests.get(url, headers=headers).content
        e = html.fromstring(r)
        pic_url = e.xpath('//div[@class="listbox"]/a/@href')
        pic_page_link.extend(pic_url)
    for page in page_href:
        url = 'http://www.5857.com' + page
        r = requests.get(url,headers=headers).content
        e = html.fromstring(r)
        pic_url = e.xpath('//div[@class="listbox"]/a/@href')
        pic_page_link.extend(pic_url)
    return pic_page_link


def pic_real_link(pic_url):
    r = requests.get(pic_url,headers=headers).content
    e = html.fromstring(r)
    page_href = e.xpath('//div[@class="page"]/a/@href')[:-1]
    for page in page_href:
        url = page
        r = requests.get(url,headers=headers).content
        e = html.fromstring(r)
        real_pic_link = e.xpath('//div[@class="desk-tit-r"]/a/@href')[0]
        i = real_pic_link.index('_')
        title = real_pic_link[i+1:].replace('/','_')
        pic_downloader(real_pic_link,title)


def pic_downloader(url,title):
    image = requests.get(url,headers=headers).content
    with open(title,'wb')as f:
        f.write(image)
    print('完成下载图片:'+ title + '  from:'+ url)


if __name__ == '__main__':

    url = 'http://www.5857.com/index.php?m=search&c=index&a=init&typeid=3&q=%E5%B4%94%E9%9B%AA%E8%8E%89'
    dir_name = input('请输入一个文件夹名：')
    os.mkdir(dir_name)
    os.chdir('./%s' % dir_name)
    try:
        page_link = pag_finder(url)
        for each in page_link:
            pic_real_link(each)
    except Exception as e :
        print(e)

