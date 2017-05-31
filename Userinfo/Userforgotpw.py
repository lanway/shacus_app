# -*- coding:utf-8 -*-
import json

from BaseHandlerh import BaseHandler
from Database.tables import User, Verification
from RegisterHandler import generate_verification_code
from messsage import message

__author__ = 'lanwei'


class Userforgotpw(BaseHandler):
    print "进入regist"
    retjson = {'code': '400', 'contents': 'None'}
    def post(self):
        type = self.get_argument('type', default='unsolved')
        if type == '12001':  # 验证手机号
            m_phone=self.get_argument('phone')
            try:
                user = self.db.query(User).filter(User.Utel == m_phone).one()
                if user:
                    code = generate_verification_code()
                    veri = Verification(
                        Vphone=m_phone,
                        Vcode=code,
                    )
                    self.db.merge(veri)
                    try:
                        self.db.commit()
                        self.retjson['code'] = '12001'  # success
                        self.retjson['contents'] = u'手机号验证成功，发送验证码'
                        message(code, m_phone)
                    except:
                        self.db.rollback()
                        self.retjson['code'] = '12002'  # Request Timeout
                        self.retjson['contents'] = u'服务器错误'
            except Exception, e:
                print e
                self.retjson['code'] = '12003'  # success
                self.retjson['contents'] = '该手机未注册'



        elif type=='12004': #验证验证码
            m_phone=self.get_argument('phone')
            code=self.get_argument('code')
            try:
               item=self.db.query(Verification).filter(Verification.Vphone==m_phone).one()
               #exist = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
               #delta = datetime.datetime.now() - exist.VT
               if item.Vcode==code:
                   #if delta>datetime.timedelta(minutes=10):
                   self.retjson['code']='12004'
                   self.retjson['contents']=u'验证码验证成功'
               else:
                   self.retjson['code']='12005'
                   self.retjson['contents']=u'验证码验证失败'
            except:
                self.retjson['code']='12006'
                self.retjson['contents']=u'该手机号码未发送验证码'

        elif type == '12007': # 修改密码
            m_phone = self.get_argument('phone')
            code = self.get_argument('code')
            m_password = self.get_argument('password')
            try:
                item = self.db.query(Verification).filter(Verification.Vphone == m_phone).one()
                if item.Vcode == code:
                    # if delta<datetime.timedelta(minutes=10):
                    user = self.db.query(User).filter(User.Utel == m_phone).one()
                    user.Upassword = m_password
                    self.db.commit()
                    self.retjson['code'] = '12007'
                    self.retjson['contents'] = u'修改密码成功'
                else:
                    self.retjson['code'] = '12005'
                    self.retjson['contents'] = u'验证码验证失败'
            except:
                self.retjson['code'] = '12008'
                self.retjson['contents'] = u'修改密码失败'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))