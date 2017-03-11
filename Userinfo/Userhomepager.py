# coding=utf-8
'''
@author 兰威
用于查看用户个人主页
'''
import json

import Userinfo.Ufuncs
from Activity.ACmodel import ACmodelHandler
from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import User, UCinfo, Appointment, UserLike, AppointEntry, ActivityEntry, \
    Activity
from Userinfo.Usermodel import userinfo_smply
class Userhomepager(BaseHandler):



    def post(self):

        # todo 还未增加图片地址,活动按时间排序
        retjson = {'code': '', 'contents': ''}
        retdata_ap = []
        ret_json_contents = {}
        retdata_ac = []
        ac = ACmodelHandler()
        ap = APmodelHandler()


        type = self.get_argument('type')
        u_id = self.get_argument('uid')
        auth_key = self.get_argument('authkey')
        u_other_id = self.get_argument('seeid')
        if type == '10801':                                    #查看个人主页
            ufuncs = Userinfo.Ufuncs.Ufuncs()
            if ufuncs.judge_user_valid(u_id, auth_key):                    #判断userID与auth_key是否匹配
                u_info = self.db.query(User).filter(User.Uid == u_other_id).one()
                #u_image_info = self.db.query(UserImage).filter(UserImage.UIuid == u_other_id).one()
                u_change_info =self.db.query(UCinfo).filter(UCinfo.UCuid == u_other_id).one()
                ret_user_info = userinfo_smply(u_info,u_change_info)
                ret_json_contents['user_info'] = ret_user_info

                exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,UserLike.ULlikedid == u_other_id,
                                                       UserLike.ULvalid ==1).all()
                if exist :
                    ret_json_contents['follow'] =True
                else:
                    ret_json_contents['follow'] = False
                # 筛选有效的约拍信息
                u_appointment_infos = self.db.query(AppointEntry).filter(AppointEntry.AEregisterID == u_other_id,
                                                                         AppointEntry.AEvalid ==1).all()
                for u_appointment_info in u_appointment_infos:
                    ap_id = u_appointment_info.AEapid
                    try:
                        ap_info = self.db.query(Appointment).filter(Appointment.APid == ap_id,
                                                                    Appointment.APvalid == True).one()
                        retdata_ap = ap.ap_Model_simply(ap_info,retdata_ap)
                    except Exception,e:
                        print e
                        retjson['code'] = '10602'
                        retjson['contents']='该约拍不存在'
                try :
                    u_spap_infos = self.db.query(Appointment).filter(Appointment.APsponsorid == u_other_id,
                                                                 Appointment.APvalid == True).all()

                    for u_spap_info in u_spap_infos:
                       retdata_ap = ap.ap_Model_simply(u_spap_info,retdata_ap)
                except Exception, e:
                    print e

                ret_json_contents['ap_info'] =retdata_ap

                #筛选有效的活动信息
                u_ac_infos = self.db.query(ActivityEntry).filter(ActivityEntry.ACEregisterid == u_other_id,
                                                                 ActivityEntry.ACEregisttvilid ==1).all()
                for u_ac_info in u_ac_infos:
                    ac_id = u_ac_info.ACEacid
                    ac_info = self.db.query(Activity).filter(Activity.ACid ==ac_id ,Activity.ACvalid == 1).all()
                    if ac_info:
                        ret_ac  = ac.ac_Model_simply(ac_info[0],'default')
                        retdata_ac.append(ret_ac)
                ret_json_contents['ac_info'] =retdata_ac
                retjson['code'] = '10601'
                retjson['contents'] =ret_json_contents

            else:
                retjson['code'] = '10600'
                retjson['contents'] ='授权码不正确'
            self.write(json.dumps(retjson, ensure_ascii=False, indent=2))






