# -*- coding: utf-8 -*-
'''
@author:兰威
'''
import base64

import time

from BaseHandlerh import BaseHandler

class Tokengenerate(BaseHandler):

    u_id = ''
    p_id = ''
    expire = 7200   #过期时间
    def __init__(self,uid,pid):
        '''

        Args:
            uid: 用户id 存在于数据库中
            pid: 设备ID 客户端发送
        '''
        self.u_id = uid
        self.p_id = pid

    #token生成
    def generate(self):
        '''

        Returns: token

        '''
        date = time.time()+self.expire
        key = '{uid}+{pid}+{date}'.format(uid = self.u_id,pid = self.p_id,date = date)
        token = base64.urlsafe_b64encode(key)
        self.redis.set(self.u_id,token)
        return token
test = Tokengenerate(1,1)
print test.generate()