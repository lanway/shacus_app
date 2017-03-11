# -*- coding:utf-8 -*-
'''
@author 兰威
@type 发送短信验证码
'''

import sys, urllib, urllib2, json
def message(code=000000,phone=00000000000):
   url = "http://imlaixin.cn/Api/send/data/json?accesskey=5025&secretkey=754c1c14fdda4935c127af9d9331447ed752de97&mobile="+phone+"&content=尊敬的追影用户您好，您的验证码为："+code+"，请不要告诉别人哦！【追影】"
   req = urllib2.Request(url)
   resp = urllib2.urlopen(req)
   str = resp.read()
   if(str):
       print(str)