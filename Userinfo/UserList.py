# -*- coding:utf-8 -*-
# 摄影师和模特的推荐列表
import json

from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Database.tables import User, UserCollection
from Userinfo import Usermodel
from Userinfo.UserImgHandler import UserImgHandler


class UserList(BaseHandler):
    retjson ={'code': '', 'contents': ''}
    def post(self):
        type = self.get_argument('type')

        # 请求摄影师模特列表
        if type == '10840':
            authkey = self.get_argument('authkey')  # 用户认证
            retdata = []
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()  # 用户本身
                if userid.Ucategory == 0:
                    self.retjson['code'] = '10841'
                    self.retjson['contents'] = '请设置您的用户类型:摄影师or模特'
                elif userid.Ucategory == 1:
                    imghandler = UserImgHandler()
                    reclist = imghandler.reclist(userid.Uid)   # 朋友的朋友列表(不包括自己)
                    try:
                        UserRec = self.db.query(User).filter(User.Uid.in_(reclist),User.Ucategory == 2).all()
                        for item in UserRec:
                            uc = self.db.query(UserCollection).filter(UserCollection.UCuser == item.Uid).all()
                            if uc[0]:  # 如果有作品集
                                retdata.append(Usermodel.rec_user_list(item))
                            else:
                                continue
                        self.retjson['code'] = '10840'
                        self.retjson['contents'] = retdata
                    except Exception, e:
                        print e
                        self.retjson['contents'] = '获取推荐列表失败'
                elif userid.Ucategory == 2:
                    imghandler = UserImgHandler()
                    reclist = imghandler.reclist(userid.Uid)  # 朋友的朋友列表(不包括自己)
                    try:
                        UserRec = self.db.query(User).filter(User.Uid.in_(reclist), User.Ucategory == 1).all()
                        for item in UserRec:
                            uc = self.db.query(UserCollection).filter(UserCollection.UCuser == item.Uid).all()
                            if uc[0]:  # 如果有作品集
                                retdata.append(Usermodel.rec_user_list(item))
                            else:
                                continue
                        self.retjson['code'] = '10840'
                        self.retjson['contents'] = retdata
                    except Exception, e:
                        print e
                        self.retjson['contents'] = '获取推荐集列表失败'
            except Exception, e:
                print e

        # 更改类型
        if type == '10842':
            authkey = self.get_argument('authkey')  # 用户认证
            category = self.get_argument('category')
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()  # 用户本身
                userid.Ucategory = category
                self.db.commit()
                self.retjson['code'] = '10842'
                self.retjson['contents'] = '修改用户类型成功'
            except Exception, e:
                print e

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
