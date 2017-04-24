# -*- coding:utf-8 -*-
import json

from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler

# 约拍伴侣
from Database.tables import ApCompanion
from FileHandler.ImageHandler import ImageHandler


class ApCompanionHandler(BaseHandler):
    retjson = {'code':'', 'contents':''}
    def post(self):
        type = self.get_argument('type')
        if type == '10900':   # 发布约拍伴侣
            ApcTitle = self.get_argument('title')
            ApcContent = self.get_argument('content')
            ApcUrl = self.get_argument('companionUrl')
            Apcimg = self.get_arguments('companionImgs[]', strip=True)

            new_ApCompanion = ApCompanion(
                ApCtitle=ApcTitle,
                ApCcontent=ApcContent,
                ApCompanionValid=1,
                ApCompanionurl=ApcUrl,
                )
            self.db.merge(new_ApCompanion)
            self.db.commit()
            try:
                OneCompanion = self.db.query(ApCompanion).filter(ApCompanion.ApCtitle == ApcTitle,
                                                        ApCompanion.ApCcontent == ApcContent,
                                                        ApCompanion.ApCompanionurl == ApcUrl,
                                                        ApCompanion.ApCompanionValid == 1).one()
                image = ImageHandler()
                image.insert_companion_image(Apcimg, OneCompanion.ApCompanionid)
                self.db.commit()
                self.retjson['code'] = '10900'
                self.retjson['contents'] = '约拍伴侣创建成功'
            except Exception, e:
                print e
                self.retjson['code']='10901'
                self.retjson['contents']='创建失败'

        elif type == '10902':  # 删除一个约拍伴侣
            Companion_id = self.get_argument('CompanionId')
            try:
                Companion_to_delete = self.db.query(ApCompanion).filter(ApCompanion.ApCompanionid == Companion_id).one()
                Companion_to_delete.ApCompanionValid = 0
                self.db.commit()
                self.retjson['code']='10902'
                self.retjson['contents']='删除成功'
            except Exception, e:
                print e
                self.retjson['code']='10903'
                self.retjson['contents']= '查找约拍伴侣失败'
        elif type == '10904':# 返回约拍伴侣
            retdata = []
            Companion_all = self.db.query(ApCompanion).filter(ApCompanion.ApCompanionValid == 1).all()
            modelhandler = APmodelHandler()
            for item in Companion_all:
                modelhandler.ApCompanion(item, retdata)

            self.retjson['code'] = '10904'
            self.retjson['contents'] = retdata


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))






