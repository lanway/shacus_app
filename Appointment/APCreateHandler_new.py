# coding=utf-8
'''
  @author:黄鑫晨
  2016.08.29   2016.09.03
'''
import json

from sqlalchemy import desc

from Appointment.APgroupHandler import APgroupHandler
from BaseHandlerh import BaseHandler
from Database.tables import Appointment, User
from FileHandler.ImageHandler import ImageHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs


class APcreateHandler(BaseHandler):  # 创建约拍
    retjson = {'code': '', 'contents': 'None'}

    def post(self):
        # 10201 客户端请求，摄影师发布约拍  start

        ap_type = self.get_argument('type')
        if ap_type == '10201' or ap_type == '10202':  # 请求获得上传权限
            print '进入10201'
            user_phone = self.get_argument('phone')
            auth_key = self.get_argument('auth_key')
            #ap_title = self.get_argument('title')
            ap_imgs = self.get_argument('imgs',)
            #print '获得图片'
            try:
                sponsor = self.db.query(User).filter(User.Utel == user_phone).one()
                print '进入try::::::'
                key = sponsor.Uauthkey
                ap_sponsorid = sponsor.Uid
                #print  'ap_sponsorid::::', ap_sponsorid
                #print 'ap_title::::', ap_title
                if auth_key == key:  # 认证成功
                    print '认证成功'
                    # retjson_body = {'auth_key': '', 'apId': ''}
                    retjson_body = {}
                    auth_key_handler = AuthKeyHandler()
                    ap_imgs_json = json.loads(ap_imgs)
                    retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)
                    self.retjson['code'] = '10200'
                    if ap_type == '10201':
                            type_ap = 1
                    elif ap_type == '10202':
                            type_ap = 0
                    self.retjson['contents'] = retjson_body
                else:
                    self.retjson['code'] = '10211'
                    self.retjson['contents'] = r'用户授权码错误'
            except Exception, e:
                print e
                self.retjson['code'] = '10212'
                self.retjson['contents'] = "该用户名不存在"
        elif ap_type == '10205':  # 开始传输数据
            print "进入10205"
            # todo ：如果完成约拍发起第一步没有完成第二步，在返回时应该过滤掉这些活动
            #ap_id = self.get_argument('apid')
            uid = self.get_argument('uid')
            auth_key = self.get_argument('auth_key')
            # todo: auth_key经常使用，可以优化
            # ap_title = self.get_argument('title')
            # ap_start_time = self.get_argument('start_time')
            # ap_end_time = self.get_argument('end_time')
            # ap_join_time = self.get_argument('join_time')
            ap_time = self.get_argument('time')
            ap_location = self.get_argument('location')
            ap_pricetag = self.get_argument('pricetag')
            #ap_free = self.get_argument('free')
            ap_price = self.get_argument('price')
            ap_content = self.get_argument('contents')
            #ap_tag = self.get_argument('tags')  # 约拍标签？确认长度
            ap_addallowed = self.get_argument('ap_allowed')
            ap_type = self.get_argument('ap_type')
            ap_imgs = self.get_argument('imgs')
            ap_group = self.get_argument('group') # 约拍分类
            ap_imgs_json = json.loads(ap_imgs)
            imghandler = ImageHandler()
            newapp = Appointment(
                        APsponsorid=uid,
                        APlocation=ap_location,
                        APtime=ap_time,
                        APcontent=ap_content,
                        APpricetag=ap_pricetag,
                        APprice=ap_price,
                        APtype=ap_type,
                        APaddallowed=ap_addallowed,
                        APgroup=ap_group
                    )
            self.db.merge(newapp)
            try:
                self.db.commit()
                if ap_imgs_json:
                    ap = self.db.query(Appointment).filter(Appointment.APcontent == ap_content).order_by(desc(Appointment.APcreateT)).all()
                    ap_id = ap[0].APid
                    imghandler.insert_appointment_image(ap_imgs_json, ap_id)
                self.retjson['code'] = '10214'
                self.retjson['contents'] = '发布约拍成功'
            except Exception, e:
                    print e, '网络故障'
                    self.retjson['contents'] = '数据库错误'
                    self.retjson['code'] = '10215'



        # 取消约拍
        elif ap_type == '10207':
            auth_key = self.get_argument('authkey')
            apid = self.get_argument('apid')
            uid = self.get_argument('userid')
            ufunc = Ufuncs()
            if ufunc.judge_user_valid(uid, auth_key):
                try:
                    appointment = self.db.query(Appointment).filter(Appointment.APid == apid).one()
                    if appointment.APvalid == 1:
                        # 约拍还有效
                        if appointment.APsponsorid == int(uid):
                            # 报名中，可以取消
                            if appointment.APstatus == 0:
                                appointment.APvalid = 0
                                self.db.commit()
                                self.retjson['code'] = '10200'
                                self.retjson['contents'] = '成功取消约拍！'
                            else:
                                self.retjson['code'] = '10215'
                                self.retjson['contents'] = '该约拍正在进行中或已完成，不能取消！'
                        else:
                            self.retjson['code'] = '10216'
                            self.retjson['contents'] = '该用户不是发起人，无权利取消'
                    else:
                        self.retjson['code'] = '10217'
                        self.retjson['contents'] = '该约拍之前已被取消！'
                except Exception ,e:
                    self.retjson['code'] = '10218'
                    self.retjson['contents'] = '该约拍不存在！'
            else:
                self.retjson['code'] = '10211'
                self.retjson['contents'] = '用户授权错误'
        else:
            print 'ap_type: ', ap_type
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))

        # 判断返回是否许可

        # 10201 客户端请求，摄影师发布约拍 end






