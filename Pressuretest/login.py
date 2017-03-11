# coding=utf-8
'''
@author：黄鑫晨
'''
import json

import tornado
from sqlalchemy import desc
from tornado import gen
from tornado.concurrent import Future
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User
from Userinfo import Usermodel
from Userinfo.Ufuncs import Ufuncs
from Userinfo.Usermodel import Model_daohanglan

class login(BaseHandler):

    retjson = {'code': '', 'contents': u'未处理 '}

    @asynchronous
    @gen.coroutine
    def post(self):
        askcode = self.get_argument('askCode')  # 请求码
        future =Future()

        if askcode == '10106':  # 手动登录
            m_phone = self.get_argument('phone')
            m_password = self.get_argument('password')
            if not m_phone or not m_password:
                self.retjson['code'] = 400
                self.retjson['contents'] = 10105  # '用户名密码不能为空'
        #todo:登录返回json的retdata多一层[]，客户端多0.5秒处理时间
        # 防止重复注册
            else:
                try:
                    user = self.db.query(User).filter(User.Utel == m_phone).one()
                    if user:  # 用户存在
                        password = user.Upassword
                        if m_password == password:  # 密码正确
                            self.get_login_model(user)
                        else:
                            self.retjson['contents'] = u'密码错误'
                            self.retjson['code'] = '10114'  # 密码错误
                    else:  # 用户不存在
                        self.retjson['contents'] = u'该用户不存在'
                        self.retjson['code'] = '10113'
                except Exception, e:  # 还没有注册
                    print "异常："
                    print e
                    self.retjson['contents'] = u'该用户名不存在'
                    self.retjson['code'] = '10113'  # '该用户名不存在'
        elif askcode == '10105':  # 自动登录
            auth_key = self.get_argument("authkey")  # 授权码
            uid = self.get_argument('uid')
            try:
                user = self.db.query(User).filter(User.Uid == uid).one()
                u_auth_key = user.Uauthkey
                if auth_key == u_auth_key:
                    self.retjson['code'] = '10111'
                    self.get_login_model(user)
                else:
                    self.retjson['code'] = '10116'
                    self.retjson['contents'] = u'授权码不正确或已过期'
            except Exception, e:
                print e
                self.retjson['code'] = '10113'
                self.retjson['contents'] = u'该用户名不存在'

        else:
            self.retjson['contents'] = u"登录类型不满足要求，请重新登录！"
            self.retjson['data'] = u"登录类型不满足要求，请重新登录！"
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.finish()

    @asynchronous
    @gen.coroutine
    def bannerinit(self):
        from FileHandler.Upload import AuthKeyHandler
        bannertokens = []

        authkeyhandler = AuthKeyHandler()
        banner1 = authkeyhandler.download_url("banner/banner1.jpg")
        banner2 = authkeyhandler.download_url("banner/banner2.jpg")
        banner3 = authkeyhandler.download_url("banner/banner3.jpg")
        banner4 = authkeyhandler.download_url("banner/banner4.jpg")
        banner_json1 = {'imgurl': banner1, 'weburl': "http://www.shacus.cn/"}
        banner_json2 = {'imgurl': banner2, 'weburl': "http://www.shacus.cn/"}
        banner_json3 = {'imgurl': banner3, 'weburl': "http://www.shacus.cn/"}
        banner_json4 = {'imgurl': banner4, 'weburl': "http://www.shacus.cn/"}
        bannertokens.append(banner_json1)
        bannertokens.append(banner_json2)
        bannertokens.append(banner_json3)
        bannertokens.append(banner_json4)
        return bannertokens

    @asynchronous
    @gen.coroutine
    def get_login_model(self, user):
        retdata = []
        user_model = Usermodel.get_user_detail_from_user(user)  # 用户模型
        photo_list = []  # 摄影师发布的约拍
        model_list = []
        try:
            photo_list_all = self.db.query(Appointment).filter(Appointment.APtype == 1,
                                                               Appointment.APvalid == 1). \
                order_by(desc(Appointment.APcreateT)).limit(6).all()
            model_list_all = self.db.query(Appointment).filter(Appointment.APtype == 0,
                                                               Appointment.APvalid == 1). \
                order_by(desc(Appointment.APcreateT)).limit(6).all()
            from Appointment.APmodel import APmodelHandler
            ap_model_handler = APmodelHandler()  # 创建对象

            ap_model_handler.ap_Model_simply(photo_list_all, photo_list, user.Uid)
            ap_model_handler.ap_Model_simply(model_list_all, model_list, user.Uid)
            data = dict(
                userModel=user_model,
                daohanglan=self.bannerinit(),
                photoList=photo_list,
                modelList=model_list,
            )
            # todo 待生成真的导航栏

            retdata.append(data)
            self.retjson['code'] = '10111'
            self.retjson['contents'] = retdata
        except Exception, e:
            print e
            self.retjson['contents'] = r"摄影师约拍列表导入失败！"