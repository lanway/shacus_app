# -*- coding: utf-8 -*-
'''
@author:黄鑫晨
'''
import urllib2
import json

def http_post():
    url='http://localhost:800/regist'
    base_nick_name = '小黄人'
    base_phone_number = '151518586'
    #for i in range(10, 60):
    try:
        nick_name = base_nick_name + str(77)
        phone_number = base_phone_number + str(78)
        print nick_name
        print phone_number
        values = {'type': '10003', 'password': '123456', 'nickName': nick_name, 'phone': phone_number}
        print nick_name
        print phone_number
        jdata = json.dumps(values)             # 对数据进行JSON格式化编码
        req = urllib2.Request(url, jdata)       # 生成页面请求的完整数据
        print req
        response = urllib2.urlopen(req)       # 发送页面请求
        print response.read()                    # 获取服务器返回的页面信息
    except Exception,e:
        print e
resp = http_post()
print resp