# -*- coding: utf-8 -*-
'''
@author:兰威
'''
import sys
sys.path.append("..")
import base64

import time

from BaseHandlerh import BaseHandler

class Tokenjudge(BaseHandler):

    s_time = ''
    token = ''
    difference  = 10000000000000000000000000000000000000000000 #用于判断请求时间的差值，判断是否由客户端发送的
    expire = 72000
    def __init__(self,stime,token,):
        '''

        Args:
            stime: 客户端传输时间
            token: 客户端传输的秘钥
        '''
        self.s_time = stime
        self.token = token

    def judge(self):
        '''

        Returns: 判断正确返回true，错误返回false

        '''
        now_time = time.time()
        difference = abs(now_time-self.s_time)
        print difference
        if difference<self.difference:
            key = base64.urlsafe_b64decode(self.token)
            key = key.split("+")
            if key[2]>now_time:
                if self.redis.get(key[0]) == self.token:
                    self.redis.expire(key[0] , self.expire)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
test = Tokenjudge(1,'MSsxKzE0OTIwMDg2NjQuODY=')
test.judge()