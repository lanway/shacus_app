# -*- coding: utf-8 -*-
'''
@author:王佳镭
@模块功能：请求所有动态
'''
import json
import TRfunction
from BaseHandlerh import BaseHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, TrendImage, Image, Favorite


class TRendspost(BaseHandler):
    retjson = {'code':'200','contents':'null'}
    def post(self):
       retdata = []
       type = self.get_argument('type',default='unsolved')
       if type == '12001':#请求刷新所有动态
           u_id = self.get_argument('uid',default='null')
           u_auth_key = self.get_argument('authkey',default='null')
           ufuncs = Ufuncs() #判断用户权限
           if ufuncs.judge_user_valid(u_id , u_auth_key):#认证成功
               data=self.db.query(Trend).all()
               favorites = self.db.query(Favorite).filter(Favorite.Fuid == u_id,Favorite.Ftype==3,
                                                          Favorite.Fvalid == 1).all()
               list=[]
               exsit=0
               for items in favorites:
                   list.append(items.Ftypeid)
                   print '哈哈哈',items.Ftypeid
               for i in range(len(data)):
                   print '哈哈哈哈',len(data)
                   try:
                       url=self.db.query(TrendImage).filter(TrendImage.TItid==data[i].Tid).one()
                       for item in list:
                           if data[i].Tid == item:
                               exsit =1
                               break
                           else:
                               exsit = 0
                       TRfunction.TRresponse(data[i],url.TIimgurl,retdata,exsit)
                   except Exception,e:
                       print e
               self.retjson['code']='12013'
               self.retjson['contents'] =retdata
           else:
               self.retjson['code']='12012'
               self.retjson['contents']='用户认证失败'


       self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

