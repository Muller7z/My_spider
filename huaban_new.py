
import os
import requests
import jsonpath

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
           ,'Accept':'application/json'
           ,'X-Request':'JSON'
           ,'X-Requested-With':'XMLHttpRequest'}
headers_img = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}


def save_img(pin_id_list):
    #pin_id_list = opener(file_name)
    dir_name = input("enter the dir_name :")
    #dir_name = "huaban"
    try:
        os.mkdir(dir_name)
    except OSError as o:
        print(o)
        pass
    os.chdir('.\\%s' % dir_name)
    for each in pin_id_list:
        find_img(each)
        #pin_id_list.remove(each)
        print("%s is done."%each)
    os.chdir('..')


def controlor(boards_id):

    id_list = save_txt(boards_id)
    save_img(id_list)


def save_txt(boards_id):
    tuple_return = find_all_pin_id(boards_id)
    #print(tuple_return)
    id_list = tuple_return[0]
    pin_count = tuple_return[1]

    if len(id_list) == pin_count:
        file_name = 'all_'+str(boards_id)+".txt"
    else:
        lack_nummber = str(pin_count-len(id_list))
        file_name = 'lack_' + lack_nummber +"_"+ str(boards_id)+".txt"
    with open(file_name,"wb")as f:
        for each in id_list:
            each = str(each) + ';'
            txt = each.encode(encoding='utf-8')
            f.write(txt)
    print("写入boardsID完成")
    return id_list


def find_img(pin_id):
    url = 'http://huaban.com/pins/%s/?jaw2dlf8' %pin_id
    # print(url)
    rsp = requests.get(url, headers=headers)
    #print(rsp.text)
    json_obj = rsp.json()
    img_key = jsonpath.jsonpath(json_obj, "$..original_pin.file.key")  # 这里就定位到了图片的key
    img_type = jsonpath.jsonpath(json_obj, '$..original_pin.file.type')  # 顺便把图片的格式提取出来
    img_id = jsonpath.jsonpath(json_obj, "$..pin_id")[0]
    img_source = jsonpath.jsonpath(json_obj, "$..source")[0]
    img_link = jsonpath.jsonpath(json_obj, "$..link")[0]
    #print(img_source)
    #print(img_link)

    if img_key == False:
        img_key = jsonpath.jsonpath(json_obj, "$..file.key")  # 上一步返回的key有一些是False，因为original可能为空
        img_type = jsonpath.jsonpath(json_obj, '$..file.type')  # 通过分析:有一些图片的key 在file目录下，那就改变一下提取出来
    img_key = img_key[0]
    img_type = img_type[0]
    img_id = str(img_id)
    i = img_type.index("/")
    img_type = img_type[i + 1:]
    # print(img_type + ':' + img_key +':'+ img_id)
    #return (img_key,img_id,img_type)
    downloader(img_key,img_id,img_type)


def downloader(key,pin_id,type):
    '''这是一个下载器，传入三个参数，构建url，得到图片，保存！'''

    url = 'http://img.hb.aicdn.com/'+key+'_fw658'  # 构建url
    try:
        img = requests.get(url,headers=headers).content
        img_name = str(pin_id)+'.'+type
        print("---------------------------------------------------------------------------------")
        print("正在下载图片：" + img_name)
        print("下载链接：" + url)
        with open(img_name,"wb")as f:  # 写入文件
            f.write(img)
    except Exception as t:
        with open("Error_logging.txt","wb")as w:
            error = str(t)+"出错了！图片链接是："+ url
            w.write(error.encode(encoding="utf-8"))  # 记录下错误日志
        pass


def find_pin_id_20(pin_id,boards_id):
    request_URL = 'http://huaban.com/boards/%s/?jbrvz3x1&max=%s&limit=20&wfl=1'%(str(boards_id),str(pin_id))
    print(request_URL)
    json_obj = requests.get(request_URL,headers = headers).json()
    #print(json_obj)
    pin_id_list = jsonpath.jsonpath(json_obj, "$..pin_id")  # jsonpath方法匹配出pinID

    if pin_id_list != False:
        #print("获取到的id个数:   "+str(len(pin_id_list)))
        int_list = []
        for each in pin_id_list:
            int_list.append(int(each))
        #print(int_list)
        return int_list
    else:
        return pin_id_list


def find_all_pin_id(boards_id):
    url = 'http://huaban.com/boards/%s/'%str(boards_id)
    rsp = requests.get(url,headers=headers)
    #print(rsp.text)
    json_obj = rsp.json()
    pin_count = jsonpath.jsonpath(json_obj, '$..pin_count')[0]
    pin_id_original = jsonpath.jsonpath(json_obj,'$..pin_id')
    #print(len(pin_id_original))
    while True:
        if len(pin_id_original) < 20:
            break
        else:
            print("---------------------------------")
            #print("开始的id:%s"%pin_id_original[-1])
            new_list = find_pin_id_20(pin_id_original[-1],boards_id)
            print("返回的id:%s"%new_list)
        if new_list == False:
            break
        if new_list == None:
            break
        pin_id_original.extend(new_list)
        if len(new_list) <20:
            break
    check_list = []
    for each in pin_id_original:
        if each not in check_list:
            check_list.append(each)
    #print(len(check_list))
    return (check_list,pin_count)


if __name__ == "__main__":
    boards_id = input("请输入画板id：")
    controlor(int(boards_id))
