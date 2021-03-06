# -*- coding:utf-8 -*-
import json


from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler

# 约拍伴侣
from Database.tables import  WApCompanions, WAcAuth
from FileHandler.ImageHandler import ImageHandler


class ApCompanionHandler(BaseHandler):
    retjson = {'code':'', 'contents':''}
    def post(self):
        type = self.get_argument('type')
        if type == '10900':   # 发布约拍伴侣
            ApcTitle = self.get_argument('title')
            ApOrc = self.get_argument('orgnazation')
            ApcContent = self.get_argument('content')
            ApcUrl = self.get_argument('companionUrl')
            Apcimg = self.get_arguments('companionImgs[]')

            new_ApCompanion = WApCompanions(
                            WAPCname=ApcTitle,
                            WAPCServeintro=ApcContent,  # 服务内容介绍
                            WAPCOrganintro=ApOrc,
                            WAPCvalid=1,
                            WAPCContact=ApcUrl,
            )

            self.db.merge(new_ApCompanion)
            self.db.commit()
            try:
                    OneCompanion = self.db.query(WApCompanions).filter(WApCompanions.WAPCname == ApcTitle,
                                                                    WApCompanions.WAPCServeintro == ApcContent,
                                                                    WApCompanions.WAPCContact == ApcUrl,
                                                                    WApCompanions.WAPCvalid == 1).one()
                    image = ImageHandler()
                    image.insert_companion_image(Apcimg, OneCompanion.WAPCid)
                    self.db.commit()
                    self.retjson['code'] = '10900'
                    self.retjson['contents'] = '约拍伴侣创建成功'
            except Exception, e:
                    print e
                    self.retjson['code']='10901'
                    self.retjson['contents']='创建失败'

        elif type == '10904':
            # 返回约拍伴侣
            retdata = []
            Companion_all = self.db.query(WApCompanions).filter(WApCompanions.WAPCvalid == 1).all()
            modelhandler = APmodelHandler()
            for item in Companion_all:
                modelhandler.ApCompanion(item, retdata)

            self.retjson['code'] = '10904'
            self.retjson['contents'] = retdata


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))






