# coding=utf-8
'''
用户点赞表
@author: 黄鑫晨
'''
import json

from tornado import gen
from tornado.web import asynchronous

from BaseHandlerh import BaseHandler
from Database.tables import Appointment, AppointLike
from Userinfo.Ufuncs import Ufuncs


class APprase(BaseHandler):
    retjson = {'code': '', 'content': ''}

    def db_commit(self, name):
        try:
            self.prase_success(name)
        except Exception, e:
            self.db_commit_fail(e)

    def prase_success(self, name):
        self.db.commit()
        self.retjson['code'] = '10600'
        self.retjson['content'] = name

    def db_commit_fail(self, e):
        print e
        self.retjson['code'] = '10606'
        self.retjson['content'] = r'数据库提交失败'

    @asynchronous
    @gen.coroutine
    def post(self):
        type = self.get_argument('type')
        type_id = self.get_argument('typeid')
        uid = self.get_argument('uid')
        u_authkey = self.get_argument('authkey')
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(uid, u_authkey):
            try:
                appointment = self.db.query(Appointment).filter(Appointment.APid == type_id).one()
                if appointment.APvalid == 0:
                    self.retjson['content'] = r"该约拍已失效"
                else:  # 查找是否已经点过赞
                    try:
                        once_liked = self.db.query(AppointLike).filter(AppointLike.ALapid == type_id, AppointLike.ALuid == uid).one()
                        if once_liked:
                                if once_liked.ALvalid == 1:  # 已经赞过
                                    if type == '10601':  # 对约拍进行点赞
                                        self.retjson['code'] = '10605'
                                        self.retjson['content'] = r'已点过赞'
                                    elif type == '10611':  # 取消赞
                                        once_liked.ALvalid = 0
                                        try:
                                            appointment.APlikeN -= 1
                                            self.db.commit()
                                            self.retjson['code'] = '10615'
                                            self.retjson['content'] = r'取消赞成功'
                                        except Exception, e:
                                            self.db_commit_fail(e)
                                else:  # 曾经点过赞，但是已经取消
                                    if type == '10601':
                                        once_liked.ALvalid = 1
                                        appointment.APlikeN += 1
                                        self.db_commit(r'点赞成功')
                                    elif type == '10611':
                                        self.retjson['code'] = '10613'
                                        self.retjson['content'] = r'用户已取消赞！'
                    except Exception, e: # 未对这个操作过
                        print e
                        if type == '10611':
                            self.retjson['code'] = '10614'
                            self.retjson['content'] = r'用户未赞过此约拍！'
                        elif type == '10601':
                            new_Aplike = AppointLike(
                                ALapid=type_id,
                                ALuid=uid,
                                ALvalid=1
                            )
                            appointment.APlikeN += 1
                            self.db.merge(new_Aplike)
                            self.db_commit(r'点赞成功')
            except Exception, e:
                    print e
                    self.retjson['code'] = '10607'
                    self.retjson['content'] = '该约拍不存在'
        else:
            self.retjson['code'] = '10608'
            self.retjson['content'] = '用户认证失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
        self.finish()