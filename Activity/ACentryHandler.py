# -*- coding:utf-8 -*-
'''
@author:王佳镭
'''
from Userinfo.Ufuncs import Ufuncs
import json
import ACFunction
import ACentryFunction
from BaseHandlerh import  BaseHandler
from Database.tables import ActivityEntry, Activity,ActivityLike


class AskEntry(BaseHandler): #活动报名点赞表相关操作
    retjson = {'code': 200, 'contents': 'none'}
    retdata = []  # list array

    def db_commit(self, name):
        try:
            self.prase_success(name)
        except Exception, e:
            self.db_commit_fail(e)

    def prase_success(self, name):
        self.db.commit()
        self.retjson['code'] = '10381'
        self.retjson['contents'] = name

    def db_commit_fail(self, e):
        print e
        self.retjson['code'] = '10380'
        self.retjson['contents'] = r'数据库提交失败'

    def post(self):



        type=self.get_argument("type",default="null")
        if type=="10309": #查看已报名活动
            m_id=self.get_argument("registerid",default = "null")
            try:
                data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == m_id).all()
                for ID in data:
                     dataask = self.db.query(Activity).filter(Activity.ACid == ID.ACEacid).all()
                     for item in dataask:
                        ACFunction.response(item, self.retdata)
                self.retjson['contents'] = self.retdata
            except Exception,e:
                print e
                self.retjson['code']=10309
                self.retjson['contents']='page failed'
        elif type=='10308':      #评价活动
            m_ACEacid=self.get_argument("aceacid",default="null")
            m_ACEregisterid=self.get_argument("aceregisterid",default="null")
            m_comments=self.get_argument("acecomment",default="null")
            try:
                ifend=self.db.query(Activity).filter(m_ACEacid==Activity.ACid).one()
                print '哈哈哈'
                print ifend.ACstatus
                if ifend.ACstatus== 2:
                    try:
                        data=self.db.query(ActivityEntry).filter(ActivityEntry.ACEacid==m_ACEacid, ActivityEntry.ACEregisterid==m_ACEregisterid).one()
                        if not data.ACEcomment:
                            data.ACEcomment=m_comments
                            self.db.commit()
                            ACentryFunction.response(data, self.retdata)
                            self.retjson['code'] = '10381'
                            self.retjson['contents'] = "评论成功"
                        else:
                            self.retjson['contents']='评论已经存在'
                            self.retjson['code']='10383'

                    except Exception,e:
                        print e
                        self.retjson["code"]='10382'
                        self.retjson["contents"]="你没有报名此活动！"
                else:
                    self.retjson['code']='10384'
                    self.retjson['contents']='活动尚未结束不能评论！'
            except Exception,e:
                    print e


        elif type=='10361'or type=='10362':
       # elif type=='10311':#活动点赞
            uid = self.get_argument('uid')
            u_authkey = self.get_argument('authkey')
            m_ACLacid=self.get_argument("aclacid",default="null")#活动的id
            ufunc = Ufuncs()
            if ufunc.judge_user_valid(uid, u_authkey):
                try:
                    print m_ACLacid
                    data=self.db.query(Activity).filter(Activity.ACid==m_ACLacid).one()
                    if data.ACvalid == 0:
                        self.retjson['contents']='活动已经失效'
                    else:
                        try:#是否已经点过赞
                            once_liked = self.db.query(ActivityLike).filter(ActivityLike.ACLacid == m_ACLacid,
                                                                           ActivityLike.ACLuid == uid).one()
                            if once_liked:
                                if once_liked.ACLvalid == 1:  # 已经赞过
                                    if type == '10361':  # 对活动进行点赞
                                        self.retjson['code'] = '10385'
                                        self.retjson['contents'] = r'已点过赞'
                                    elif type == '10362':  # 取消赞
                                        once_liked.ACLvalid = 0
                                        try:
                                            data.AClikenumber -= 1
                                            self.db.commit()
                                            self.retjson['code'] = '10386'
                                            self.retjson['contents'] = r'取消赞成功'
                                        except Exception, e:
                                            self.db_commit_fail(e)
                                else:  # 曾经点过赞，但是已经取消
                                    if type == '10361':
                                        print '进来了啊啊啊啊'
                                        once_liked.ACLvalid = 1
                                        data.AClikenumber =data.AClikenumber+ 1
                                        print data.AClikenumber
                                        self.db_commit(r'点赞成功')
                                        self.retjson['code'] = '10387'
                                        self.retjson['contents'] = r'点赞成功'
                                    elif type == '10362':
                                        self.retjson['code'] = '10386'
                                        self.retjson['contents'] = r'用户已取消赞！'
                        except Exception, e:  # 未对这个操作过
                              print e
                              if type == '10362':
                                    self.retjson['code'] = '10390'
                                    self.retjson['contents'] = r'用户未赞过此活动！'
                              elif type == '10361':
                                    new_Aclike = ActivityLike(
                                        ACLacid=m_ACLacid,
                                        ACLuid=uid,
                                        ACLvalid=1,
                                    )
                                    print 'aaaa进来了哦哦哦'
                                    print 'now number is',data.AClikenumber
                                    data.AClikenumber += 1
                                    print '+1num',data.AClikenumber
                                    self.db.merge(new_Aclike)
                                    self.db_commit(r'点赞成功')
                                    self.retjson['code'] = '10387'
                                    self.retjson['contents'] = '点赞成功'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10391'
                    self.retjson['contents'] = '该活动不存在'
            else:
                    self.retjson['code'] = '10392'
                    self.retjson['contents'] = '用户认证失败'

        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文



