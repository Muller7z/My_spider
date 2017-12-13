import requests
from lxml import html
import os
import time

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

jsjlq = {'pag_url':'//tr[@class="tr3 t_one tac"]/td/h3/a/@href',
        'img_url':'//img[@style="cursor:pointer"]/@src',
        'title':'//tr[@class="tr1 do_not_catch"]//h4/text()'}  # 技术讨论区的path


def find_pag_url(pag):
    '''从首页找到分页的url'''
    url = 'http://youkezjz.ml/thread0806.php?fid=16&search=&page='+str(pag)
    rsp = requests.get(url,headers=headers).text
    elm = html.fromstring(rsp)
    pag_url_list = elm.xpath('//tr[@class="tr3 t_one tac"]/td/h3/a/@href')
    for each in pag_url_list:
        url = 'http://youkezjz.ml/'+each
        try:
            find_img_url(url)   # 调用图片地址查找器
        except IndexError as i:
            print(i)


def find_img_url(url):
    '''图片地址查找器  找到此页面下所有图片的url，和标题'''
    rsp = requests.get(url, headers=headers).content
    elm = html.fromstring(rsp)
    '''以下的xpath路径可以解析出绝大部分图片url地址'''
    path_list = ['//div[@class="tpc_content do_not_catch"]/input/@src','//tr[@class="tr3"]//input/@src',
                 '//div[@class="tpc_content do_not_catch"]//input/@src']
    img_url = elm.xpath(path_list[0])
    if img_url == []:
        img_url = elm.xpath(path_list[1])
        if img_url == []:
            img_url = elm.xpath(path_list[2])

    title = elm.xpath('//tr[@class="tr1 do_not_catch"]//h4/text()')[0]  # 解析出title
    print(title)
    print(len(img_url))
    print(img_url)
    if len(img_url) <=5:   # 筛除图片数量小于5的页面
        print("没有找到")
    else:
        os.chdir("D:\TEST")

        try:                   # 可能会发生os错误
            os.mkdir(title)
            os.chdir("D:\TEST\\" + title)
        except OSError as o:
            time_name = time.time()  # 用时间来代替文件名
            os.mkdir("文件名错误"+str(time_name))
            os.chdir("D:\TEST\\文件名错误"+str(time_name))
            print(o)

        #for i in range(5):
        for i in range(len(img_url)):
            url = img_url[i]
            name = title + "_%s" % i + '.jpg'
            img_downloader(url, name)  # 调用图片下载器
        os.chdir("D:\TEST")


def img_downloader(url,name):
    '''图片下载器'''
    try:  # 可能会联接超时，可以增加timeout限制时间尽可能获取图片
        rsp = requests.get(url, timeout=2,headers=headers).content
        print('正在下载图片：'+name)
        with open(name,"wb")as f:
            f.write(rsp)
    except Exception as t:
        with open("Error_logging.txt","wb")as f:
            error = str(t)+"联接超时，图片链接是："+ url
            f.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        pass


if __name__ == "__main__":
    find_pag_url(1)
    # find_img_url('http://youkezjz.ml/htm_data/7/1711/2812095.html')
    # img_downloader('http://img181.poco.cn/mypoco/myphoto/20110609/15/56246126201106091521252161896605963_012.jpg',"test.jpg")
