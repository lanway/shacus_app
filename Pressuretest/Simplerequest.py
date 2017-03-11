# -*- coding: utf-8 -*-
'''
@author:黄鑫晨
'''
import json

from sqlalchemy import desc
from tornado import gen
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import User, Appointment
from Userinfo.Usermodel import Model_daohanglan


class Simplerequest(BaseHandler):
        retjson = {'code': '', 'contents': u'未处理 '}
        @asynchronous
        @gen.coroutine
        def post(self):
            askcode = self.get_argument('askCode')  # 请求码
            m_phone = self.get_argument('phone')
            if askcode == '10106':  # 手动登录
                m_password = self.get_argument('password')
                if not m_phone or not m_password:
                    self.retjson['code'] = 400
                    self.retjson['contents'] = 10105  # '用户名密码不能为空'
                    # todo:登录返回json的retdata多一层[]，客户端多0.5秒处理时间
                    # 防止重复注册
                else:
                    try:
                        user = self.db.query(User).filter(User.Utel == m_phone).one()
                        if user:  # 用户存在
                            password = user.Upassword
                            if m_password == password:  # 密码正确
                                print u'密码正确'
                                self.retjson['code'] = 200
                                if user.Ubirthday:
                                    Ubirthday = user.Ubirthday.strftime('%Y-%m-%d %H:%M:%S'),
                                else:
                                    Ubirthday = ''
                                retdata = []
                                u_auth_key = user.Uauthkey
                                user_model = dict(
                                    id=user.Uid,
                                    phone=user.Utel,
                                    nickName=user.Ualais,
                                    realName=user.Uname,
                                    sign=user.Usign,
                                    sex=user.Usex,
                                    score=user.Uscore,
                                    location=user.Ulocation,
                                    birthday=Ubirthday,
                                    registTime=user.UregistT.strftime('%Y-%m-%d %H:%M:%S'),
                                    mailBox=user.Umailbox,
                                    headImage=r"http://img5.imgtn.bdimg.com/it/u=1268523085,477716560&fm=21&gp=0.jpg",
                                    auth_key=u_auth_key
                                )
                                photo_list = []  # 摄影师发布的约拍
                                model_list = []
                                daohangl_list = []
                                daohangl_list.append(Model_daohanglan(
                                    'http://img3.imgtn.bdimg.com/it/u=4271053251,2424464488&fm=21&gp=0.jpg','www.baidu.com'))
                                daohangl_list.append(
                                    Model_daohanglan('http://image8.360doc.com/DownloadImg/2010/04/0412/2762690_45.jpg',
                                                     'http://image.baidu.com/search/detail?ct=503316480&z=0&ipn=d&word=%E7%BE%8E%E5%9B%BE&step_word=&hs=0&pn=24&spn=0&di=14293150190&pi=0&rn=1&tn=baiduimagedetail&is=&istype=0&ie=utf-8&oe=utf-8&in=&cl=2&lm=-1&st=undefined&cs=2860350365%2C3214019191&os=289517539%2C4157278886&simid=0%2C0&adpicid=0&ln=1992&fr=&fmq=1472885603080_R&fm=&ic=undefined&s=undefined&se=&sme=&tab=0&width=&height=&face=undefined&ist=&jit=&cg=&bdtype=0&oriquery=&objurl=http%3A%2F%2Fimage8.360doc.com%2FDownloadImg%2F2010%2F04%2F0412%2F2762690_45.jpg&fromurl=ippr_z2C%24qAzdH3FAzdH3Fooo_z%26e3Bnma15v_z%26e3Bv54AzdH3Fv5gpjgpAzdH3F8aAzdH3FabdaAzdH3F88AzdH3F8nad0dl_9098dc0d_z%26e3Bfip4s&gsm=0&rpstart=0&rpnum=0'))
                                try:
                                    print 'shaixuanqian'

                                    photo_list_all = self.db.query(Appointment).filter(Appointment.APtype == 1,
                                                                                       Appointment.APvalid == 1). \
                                        order_by(desc(Appointment.APcreateT)).limit(6).all()
                                    model_list_all = self.db.query(Appointment).filter(Appointment.APtype == 0,
                                                                                       Appointment.APvalid == 1). \
                                        order_by(desc(Appointment.APcreateT)).limit(6).all()
                                    from Appointment.APmodel import APmodelHandler
                                    ap_model_handler = APmodelHandler()  # 创建对象
                                    print 'chuangjianchengg'

                                    ap_model_handler.ap_Model_simply(photo_list_all, photo_list, user.Uid)

                                    ap_model_handler.ap_Model_simply(model_list_all, model_list, user.Uid)
                                    print 'shaixuanchengg'
                                    data = dict(
                                        userModel=user_model,
                                        daohanglan=daohangl_list,
                                        photoList=photo_list,
                                        modelList=model_list,
                                    )
                                    # todo 待生成真的导航栏

                                    retdata.append(data)
                                    self.retjson['code'] = '10101'
                                    self.retjson['contents'] = retdata
                                except Exception, e:
                                    print e
                                    self.retjson['contents'] = r"摄影师约拍列表导入失败！"

                            else:
                                self.retjson['contents'] = u'密码错误'
                                self.retjson['code'] = '10104'  # 密码错误
                        else:  # 用户不存在
                            self.retjson['contents'] = u'该用户不存在或服务器错误'
                            self.retjson['code'] = '10103'
                    except Exception, e:  # 还没有注册
                        print "异常："
                        print e
                        self.retjson['contents'] = u'该用户名不存在'
                        self.retjson['code'] = '10103'  # '该用户名不存在'
            elif askcode == '10105':  # 自动登录
                authcode = self.get_argument("authcode")  # 授权码
            else:
                self.retjson['contents'] = u"登录类型不满足要求，请重新登录！"
                self.retjson['data'] = u"登录类型不满足要求，请重新登录！"
            self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
            self.finish()




