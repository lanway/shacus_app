# -*- coding:utf8 -*-
import json

import Userinfo.Ufuncs
from BaseHandlerh import BaseHandler
from Database.tables import AppointmentImage
from FileHandler.Upload import AuthKeyHandler
from rongcloud import RongCloud


class Sysmessage(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}

    #向用户发送一条信息，同时弹出一个小灰条
    def post(self):
        userid = self.get_argument('userid')
        u_auth_key = self.get_argument('authkey')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(userid, u_auth_key):
            rcloud = RongCloud("x4vkb1qpvxu4k", "EziWuNBddbcfz")
            fromuserid = self.get_argument('fromuserid')
            touserid = self.get_argument('touserid')
            objectname = 'RC:ImgTextMsg'
            title = self.get_argument('title')
            content_item = self.get_argument('content')
            appid = self.get_argument('appid')
            url = 'www.baidu.com'
            extra = 'hello'
            content = {}
            imageurl = 'default.jpg'
            authkey_handler = AuthKeyHandler()
            try:
                app = self.db.query(AppointmentImage).filter(AppointmentImage.APIapid == appid).all()
                if app:
                    imageurl = app[0].APIurl
                content['title'] = title
                content['content'] = content_item
                content['imageUri'] = authkey_handler.download_originpic_url(imageurl)
                content['url'] = url
                content['extra'] = extra
                content_json = json.dumps(content,ensure_ascii=False, indent=2)
                Response = rcloud.Message.PublishSystem(fromuserid, touserid, objectname, content_json,pushContent=['push{this is new appointment}'],)
                if Response.result['code'] == 200:
                    content_sys = {"message":"您有一条新约拍","extra":""}
                    rcloud.Message.PublishSystem(fromuserid,touserid,'RC:InfoNtf',json.dumps(content_sys))
                    self.retjson['code'] = '...'
                    self.retjson['contents'] = '...'
                else:
                    print 'cucucucu'
                    self.retjson['code'] = '...'
                    self.retjson['contents'] = '...'

            except Exception,e:
                print e
                self.retjson['code'] = '...'
                self.retjson['contents'] = '...'
        else:
            self.retjson['code'] = '10521'
            self.retjson['contents'] = r'用户认证错误！操作失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))




