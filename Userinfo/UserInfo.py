# coding=utf-8
'''
@author 兰威
@type 用于获取用户基本信息
'''
import json

import Ufuncs
from BaseHandlerh import BaseHandler
from Database.tables import User, UCinfo, UserImage, Image
from Usermodel import userinfo_smply
from FileHandler.Upload import AuthKeyHandler

class UserInfo(BaseHandler):  #获取用户自己的ID

    retjson = {'code': '', 'contents': ''}
    def post(self,):
        type = self.get_argument('type')
        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, auth_key):
            if type =='10701':

                ret_content_json={}

               #判断用户是否有效
                try:
                   u_info = self.db.query(User).filter(User.Uid == u_id).one()
                   u_change_info = self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
                   #u_image = self.db.query(UserImage).filter(UserImage.UIuid == u_id).one()

                   ret_info = userinfo_smply(u_info,u_change_info)
                   ret_content_json['usermodel'] = ret_info
                   self.retjson['code'] ='10703'
                   self.retjson['contents'] = ret_content_json
                except Exception,e:
                    print e
                    self.retjson['code'] = '10702'
                    self.retjson['content'] ='用户ID不正确'
            if type =='10705':
                auth = AuthKeyHandler()
                other_id = self.get_argument('seeid')
                user_headimages = self.db.query(UserImage).filter(UserImage.UIuid == other_id).all()
                userimg = []
                for user_headimage in user_headimages:
                    exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid, Image.IMvalid == 1).all()
                    if exist:
                        userimg = user_headimage
                        break;
                ret_content={}
                user = self.db.query(User).filter(User.Uid == other_id).one()

                ret_content['uid'] = user.Uid
                ret_content['ualais']  = user.Ualais
                ret_content['uheadimage'] = auth.download_url(userimg.UIurl)
                self.retjson['code']  = '10706'
                self.retjson['contents'] = ret_content

        else :
                self.retjson['code'] = '10704'
                self.retjson['contents'] = '用户授权码不正确'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
