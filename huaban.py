# 作者是一个爬虫新手，第一次写动态页面爬虫
# 一不小心就弄了200多行代码...
# 某些情况下不能获取到某画板下全部的图片，嗯...这是个问题...
# 若此程序被各路大神看到，轻喷...
# 这是在Python3环境下运行的，引入的库也是基于Python3的，若需要在Python2中使用，需要修改相应的库和代码...

import requests,json,jsonpath,re,os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def get_pin_id(boards_id,pin_id):
    '''
    传入参数boardsID和pinID
    根据参数构建url
    发送请求，正则解析返回的html
    提取出html里的json数据
    解析json，得到pinID列表
    返回pinID列表
    '''
    if pin_id == '':
        url = 'http://huaban.com/boards/'+str(boards_id)+'/'
    else:url = 'http://huaban.com/boards/'+str(boards_id)+'/?jaul4qom&max='+str(pin_id)+'&limit=20&wfl=1'  # 构建的url
    #print(url)
    try:
        rsp = requests.get(url,headers=headers,timeout=4).content
        string = str(rsp,encoding='utf-8')  # utf-8编码字符串
        #print("匹配前"+string)
        pattern = re.compile('app\.page\["board"] = (.*?)app\._csr', re.S)  # 构建正则匹配对象
        target = pattern.findall(string)    # findall方法匹配
        #print("匹配后"+str(target))
        pin_id = target[0]
        pin_id_format = pin_id[0:-2]    # 匹配有多余的字符串，通过字符串切片提取目标 字符串
        #print(pin_id_format)
        json_obj = json.loads(pin_id_format)    # 加载为json格式
        pin_id_list = jsonpath.jsonpath(json_obj,"$..pin_id")   # jsonpath方法匹配出pinID
        pin_count = jsonpath.jsonpath(json_obj, '$..pin_count')[0]
        print('******************')
        print("本次获取到%s个"%len(pin_id_list))
        print("画板下共有%s张图片"%pin_count)
        # print(pin_id_list)
        return pin_id_list
    except Exception as t:
        with open("Error_logging.txt", "wb")as w:
            error = str(t) + "出错了！"
            w.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        pass


def find_boards_id(url):
    rsp = requests.get(url, headers=headers, timeout=4).content
    string = str(rsp, encoding='utf-8')  # utf-8编码字符串
    #print("匹配前"+string)
    pattern = re.compile('app\.page\["pins"] = (.*?)app\.page\["ads"]', re.S)  # 构建正则匹配对象
    target = pattern.findall(string)  # findall方法匹配
    #print("匹配后"+str(target))
    boards_id = target[0]
    boards_id_format = boards_id[0:-2]  # 匹配有多余的字符串，通过字符串切片提取目标 字符串
    #print(boards_id_format)
    json_obj = json.loads(boards_id_format)  # 加载为json格式
    boards_id_list = jsonpath.jsonpath(json_obj, "$..board_id")  # jsonpath方法匹配出pinID
    full_list = []
    for each in boards_id_list:
        if each not in full_list:
            full_list.append(each)
    print("本次获取到%s个画板ID" % len(full_list))
    return full_list


def find_dirname(boards_id):
    '''这里是为了找到三个参数：title、username、pin_count  ，依然是重复造轮子。。。'''

    url = 'http://huaban.com/boards/' + boards_id + '/'
    #print(url)
    rsp = requests.get(url, headers=headers, timeout=4).content
    string = str(rsp, encoding='utf-8')
    # print("匹配前"+string)
    pattern = re.compile('app\.page\["board"] = (.*?)app\._csr', re.S)
    target = pattern.findall(string)
    dirname = target[0]
    dirname_format = dirname[0:-2]
    print(dirname_format)
    json_obj = json.loads(dirname_format)
    dir_name = jsonpath.jsonpath(json_obj,"$..title")[0]
    user_name = jsonpath.jsonpath(json_obj,'$..username')[0]
    pin_count = jsonpath.jsonpath(json_obj, '$..pin_count')[0]
    print(dir_name,user_name,pin_count)
    return [dir_name,user_name,pin_count]


def get_all_id(boards_id):
    '''
    这个函数完成主要的逻辑操作，通过不断发起请求，获取到pinID
    :param boards_id:
    :return: 返回所有的pinID
    '''
    id_list = get_pin_id(boards_id, "")
    pin_count = find_dirname(boards_id)[2]
    '''调用上一步构建的get函数，得到一个初始的ID列表'''
    full_id = []    # 作初始化
    new_list = []
    while True:  # 逻辑：当返回的newlist 元素个数小于20的时候，继续调用get函数，否则就跳出循环
        pin_id = id_list[-2]
        #print(pin_id)
        check = new_list
        new_list = get_pin_id(boards_id, pin_id)  # 调用get函数获取newlist
        #if new_list != None:
        if new_list == None:
            break
        else:
            id_list.extend(new_list)
            if len(new_list) < 20:  # 跳出循环
                break
            if new_list == check:
                break
            print(len(id_list))

    for each in id_list:    # 这里是做列表去重，有可能获取到重复值，保险一点。。。
        if int(each) not in full_id:
            full_id.append(each)
    print("抓取到" + str(len(full_id))+"个ID")
    #print(full_id)
    if int(pin_count) == len(full_id):
        file_name = "all(%s)_%s.txt"%(pin_count,boards_id)
    else:
        file_name = "lack(%s)_%s.txt"%(pin_count,boards_id)
    with open(file_name,"wb")as f:
        for each in full_id:
            each = str(each) + ';'
            txt = each.encode(encoding='utf-8')
            f.write(txt)
    print("写入boardsID完成")
    return full_id


def spider_control(boards_id):
    '''这里构建了一个控制器，调用各个函数'''
    return_list = find_dirname(boards_id)
    dir_name = return_list[0]
    user_name = return_list[1]
    file_name = user_name + "_采集到_" + dir_name
    os.chdir('.\\huaban')   # 操作目录
    id_list = get_all_id(boards_id)
    try:
        os.mkdir(file_name)
    except OSError as o:
        file_name = str(boards_id)
        os.mkdir(file_name)
        print(o)
    os.chdir('.\\%s'%file_name)
    for i in range(len(id_list)):
        find_key(id_list[i])  # 调用find_key函数
        print("完成第%s/%s张"%(i+1,len(id_list)))
    os.chdir('..')


def find_key(pin_id):
    '''
    这个函数通过pinID来找到图片的key，因为下载图片的参数有key
    和get函数差不多，也是重复造轮子。。。
    '''
    url = 'http://huaban.com/pins/%s/?jaw2dlf8'%pin_id
    #print("url="+ url)
    try:
        rsp = requests.get(url,headers=headers).content

        string = str(rsp, encoding='utf-8')
        #print("匹配前"+string)
        pattern = re.compile('app\.page\["pin"] = (.*?)app\.page\["stores"]', re.S)
        target = pattern.findall(string)
        #print("匹配后" + str(target))
        key = target[0]
        key_fromat = key[0:-2]
        json_obj = json.loads(key_fromat)
        img_key = jsonpath.jsonpath(json_obj, "$..original_pin.file.key")  # 这里就定位到了图片的key
        img_type = jsonpath.jsonpath(json_obj,'$..original_pin.file.type')  # 顺便把图片的格式提取出来
        if img_key == False:
            img_key = jsonpath.jsonpath(json_obj, "$..file.key")  # 上一步返回的key有一些是False，因为original可能为空
            img_type = jsonpath.jsonpath(json_obj, '$..file.type')  # 通过分析:有一些图片的key 在file目录下，那就改变一下提取出来
        img_key = img_key[0]
        img_type = img_type[0]
        i = img_type.index("/")
        img_type = img_type[i+1:]   # 返回的图片格式如：type/jpeg  需要加工一下...用字符串切片来提取
        #print(img_key)
        #print(img_type)
        downloader(img_key, pin_id, img_type)  # 调用downloer函数
    except Exception as t:
        with open("Error_logging.txt", "wb")as w:
            error = str(t) + "出错了！图片链接是：" + url
            w.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        pass


def downloader(key,pin_id,type):
    '''这是一个下载器，传入三个参数，构建url，得到图片，保存！'''

    url = 'http://img.hb.aicdn.com/'+key+'_fw658'  # 构建url
    try:
        img = requests.get(url,headers=headers).content
        img_name = str(pin_id)+'.'+type
        print("正在下载图片：" + img_name)
        print("下载链接：" + url)
        with open(img_name,"wb")as f:  # 写入文件
            f.write(img)
    except Exception as t:
        with open("Error_logging.txt","wb")as w:
            error = str(t)+"出错了！图片链接是："+ url
            w.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        pass
    '''关于错误处理：前面获取pinID需要人工监视一下，后面的获取key和下载就可以机器自动忽略错误啦'''


if __name__ == "__main__":
    '''
    boards_id_list = find_boards_id('http://huaban.com/favorite/beauty/')
    for i in range(2,6):
        print("-------------->>>>>>")
        spider_control(boards_id_list[i])
    '''
    url = 'http://huaban.com/boards/481662/'
    boards_id = re.compile(r'\d{6}').findall(url)[0]
    print(boards_id)
    spider_control(boards_id)

