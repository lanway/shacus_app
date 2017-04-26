# -*- coding:utf8 -*-
import json

import Userinfo.Ufuncs
from BaseHandlerh import BaseHandler
from Database.tables import AppointmentImage, Appointment
from FileHandler.Upload import AuthKeyHandler
from rongcloud import RongCloud


class Sysmessage(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}

    #向用户发送一条信息，同时弹出一个小灰条
    def post(self):
        userid = self.get_argument('userid')
        u_auth_key = self.get_argument('authkey')
        request_type = self.get_argument('type')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(userid, u_auth_key):
            if request_type == '11524':   # 用户报名时给发送约拍方发送图文消息
                rcloud = RongCloud("x4vkb1qpvxu4k", "EziWuNBddbcfz")
                fromuserid = self.get_argument('fromuserid')
                touserid = self.get_argument('touserid')
                objectname = 'RC:ImgTextMsg'
                title = "有人想和你约拍"
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
                    appitem = self.db.query(Appointment).filter(Appointment.APid == appid).one()
                    content_item = appitem.APcontent
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
                        self.retjson['code'] = '11524'
                        self.retjson['contents'] = '发送消息成功'
                    else:
                        print 'cucucucu'
                        self.retjson['code'] = '11523'
                        self.retjson['contents'] = '发送消息错误'

                except Exception,e:
                    print e
                    self.retjson['code'] = '11522'
                    self.retjson['contents'] = '服务器错误'
        else:
            self.retjson['code'] = '11521'
            self.retjson['contents'] = r'用户认证错误！操作失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))




