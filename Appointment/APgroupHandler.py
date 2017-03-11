# -*- coding:utf-8  -*-
from BaseHandlerh import BaseHandler
from Database.models import get_db
from Database.tables import Appointment


class APgroupHandler(object):

    def GetGroupId(cls):
        retdata = []
        for x in range(5):
            apdata = {'type':'','apid':[]}
            ap=get_db().query(Appointment).filter(Appointment.APgroup == x+1).all()

            if x+1 == 1:
                apdata['type']='写真客片'
            elif x+1 == 2:
                apdata['type'] = '记录随拍'
            elif x+1 == 3:
                apdata['type'] = '练手互免'
            elif x+1 == 4:
                apdata['type'] = '活动跟拍'
            elif x+1 == 5:
                apdata['type'] = '商业拍摄'

            for item in ap:
                apdata['apid'].append(item.APid)
            retdata.append(apdata)
        return retdata

    @staticmethod
    def GetGroupNum(groupid):
        if groupid=='写真客片':
            return 1
        elif groupid=='记录随拍':
            return 2
        elif groupid == '练手互免':
            return 3
        elif groupid == '活动更拍':
            return 4
        elif groupid == '商业跟拍':
            return 5

    @staticmethod
    def Group():
        retdata = []
        apdata1 = {'type': '1', 'name' : '写真客片'}
        retdata.append(apdata1)
        apdata2 = {'type': '2', 'name': '记录随拍'}
        retdata.append(apdata2)
        apdata3 = {'type': '3', 'name': '练手互免'}
        retdata.append(apdata3)
        apdata4 = {'type': '4', 'name': '活动跟拍'}
        retdata.append(apdata4)
        apdata5 = {'type': '5', 'name': '商业跟拍'}
        retdata.append(apdata5)

        return retdata
