# coding=utf-8
import json

import Userinfo.Ufuncs
from Activity import ACFunction
from Appointment.APmodel import APmodelHandler
from BaseHandlerh import BaseHandler
from Database.tables import Favorite, Appointment, Activity, User, ActivityImage, UserImage, Image

'''
@author:黄鑫晨，王佳镭
@type:用户收藏
@time:2019-09-02
@attention:由于每次插入时有当前时间项，所以merge无法避免重复，仍需要判断
'''
class UserFavorite(BaseHandler):
    retjson = {'code': '', 'contents': ''}
    '''
     用户收藏表
    '''
    def not_in_fav_list(self):
        self.retjson['code'] = '10528'
        self.retjson['contents'] = r"该用户未收藏此约拍"


    def post(self):
        type = self.get_argument('type')
        user_id = self.get_argument('uid')
        u_auth_key = self.get_argument('authkey')
        ufuncs = Userinfo.Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(user_id, u_auth_key):
            if type == '10501':  # 收藏约拍
                typeid = self.get_argument('typeid')
                try:
                    exist = self.db.query(Appointment).filter(Appointment.APid == typeid).one()  # 约拍是否存在
                    if exist: # 该约拍存在
                        if exist.APvalid == 1: # 该约拍还有效
                            try:  # 判断用户曾经是否对改约拍进行过收藏动作，
                                once_favorite = self.db.query(Favorite).filter(Favorite.Fuid == user_id,
                                                                              Favorite.Ftypeid == typeid,
                                                                               Favorite.Ftype == 1).one()
                                if once_favorite: # 已有这项，不知是否有效
                                    if once_favorite.Fvalid == 0:   # 曾经收藏过，但是现在取消了
                                        once_favorite.Fvalid = 1
                                        self.db.commit()
                                        self.retjson['code'] = '10520'
                                        self.retjson['contents'] = "收藏成功"
                                    else: # 用户已收藏
                                            self.retjson['code'] = '10527'
                                            self.retjson['contents'] = "该约拍已在用户收藏夹中"

                            except Exception, e:  # 未收藏过
                                    favorite = Favorite(
                                         Fuid=user_id,
                                         Ftype=1,  # 1为约拍
                                         Ftypeid=typeid,
                                         Fvalid=1
                                    )
                                    self.db.merge(favorite)
                                    try:
                                        self.db.commit()
                                        self.retjson['code'] = '10520'
                                        self.retjson['contents'] = r'收藏成功'
                                    except Exception, e:
                                        # todo 基本码待定
                                        print e
                                        self.retjson['contents'] = r'数据库操作失败，请重试'
                        else:
                            self.retjson['code'] = '10525'
                            self.retjson['contents'] = r'该约拍已过期'
                except Exception, e:
                    print e
                    self.retjson['code'] = '10524'
                    self.retjson['contents'] = r'该约拍不存在！'
            if type == '10510':  # 取消收藏约拍
                typeid = self.get_argument('typeid')
                #todo：是否要判断该约拍是否过期？
                try:
                    #用户收藏了该约拍，可以取消
                    try:
                        once_favorite = self.db.query(Favorite).filter(Favorite.Ftype == 1, Favorite.Ftypeid == typeid, Favorite.Fuid == user_id).one()
                        if once_favorite.Fvalid == 1:  #目前还在收藏夹中
                            try:
                                self.db.query(Favorite).filter(Favorite.Fuid == user_id, Favorite.Ftypeid == typeid). \
                                    update({Favorite.Fvalid: 0}, synchronize_session=False)
                                self.db.commit()
                                self.retjson['code'] = '10523'
                                self.retjson['contents'] = r'取消收藏约拍成功'
                            except Exception, e:
                                print e
                                self.retjson['contents'] = r'数据库提交失败'
                        else:  # 曾经收藏过，但是已经取消了
                            self.not_in_fav_list()
                    except Exception,e:
                        self.not_in_fav_list()
                except Exception,e:
                    self.not_in_fav_list()


            if type == '10541': # 查看所有收藏的约拍
                retdata = []
                try:
                    favorites = self.db.query(Favorite).filter(Favorite.Fuid == user_id, Favorite.Fvalid == 1,Favorite.Ftype == 1).all()  # 返回收藏列表
                    ap_favorates = []
                    for each_favorite in favorites:
                        ap_favorite_id = each_favorite.Ftypeid  # 即约拍Id
                        ap_favorite = self.db.query(Appointment).filter(Appointment.APid == ap_favorite_id).one()
                        ap_favorates.append(ap_favorite)
                    APmodelHandler.ap_Model_simply(ap_favorates, retdata, user_id)
                    self.retjson['code'] = '10550'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    print e
                    self.retjson['code'] = '10526'
                    self.retjson['contents'] = r'用户未收藏任何约拍'

            if type == '10502':#收藏活动
                    typeid = self.get_argument('typeid')#活动id
                    try:
                        exist = self.db.query(Activity).filter(Activity.ACid == typeid).one()  #活动是否存在
                        if exist:  # 该约拍存在
                            if exist.ACvalid == 1:  # 该活动还有效
                                try:  # 判断用户曾经是否对活动拍进行过收藏动作，
                                    once_favorite = self.db.query(Favorite).filter(Favorite.Fuid == user_id,
                                                                                   Favorite.Ftypeid == typeid,
                                                                                   Favorite.Ftype == 2).one()
                                    if once_favorite:  # 已有这项，不知是否有效
                                        if once_favorite.Fvalid == 0:  # 曾经收藏过，但是现在取消了
                                            once_favorite.Fvalid = 1
                                            self.db.commit()
                                            self.retjson['code'] = '10520'
                                            self.retjson['contents'] = "收藏成功"
                                        else:  # 用户已收藏
                                            self.retjson['code'] = '10527'
                                            self.retjson['contents'] = "该活动已在用户收藏夹中"

                                except Exception, e:  # 未收藏过
                                    favorite = Favorite(
                                        Fuid=user_id,
                                        Ftype=2,  # 1为约拍
                                        Ftypeid=typeid,
                                        Fvalid=1
                                    )
                                    self.db.merge(favorite)
                                    try:
                                        self.db.commit()
                                        self.retjson['code'] = '10520'
                                        self.retjson['contents'] = r'收藏成功'
                                    except Exception, e:
                                        # todo 基本码待定
                                        print e
                                        self.retjson['contents'] = r'数据库操作失败，请重试'
                            else:
                                self.retjson['code'] = '10525'
                                self.retjson['contents'] = r'该活动已过期'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '10524'
                        self.retjson['contents'] = r'该活动不存在！'

            if type == '10511':  # 取消收藏活动
                typeid = self.get_argument('typeid')#活动id
                # todo：是否要判断该活动是否过期？
                try:
                    # 用户收藏了该约拍，可以取消
                    try:
                        once_favorite = self.db.query(Favorite).filter(Favorite.Ftype == 2, Favorite.Ftypeid == typeid,
                                                                       Favorite.Fuid == user_id).one()
                        if once_favorite.Fvalid == 1:  # 目前还在收藏夹中
                            try:
                                self.db.query(Favorite).filter(Favorite.Fuid == user_id, Favorite.Ftypeid == typeid). \
                                    update({Favorite.Fvalid: 0}, synchronize_session=False)
                                self.db.commit()
                                self.retjson['code'] = '10523'
                                self.retjson['contents'] = r'取消收藏活动成功'
                            except Exception, e:
                                print e
                                self.retjson['contents'] = r'数据库提交失败'
                        else:  # 曾经收藏过，但是已经取消了
                            self.not_in_fav_list()
                    except Exception, e:
                        self.not_in_fav_list()
                except Exception, e:
                    self.not_in_fav_list()

            if type == '10542':  # 查看所有收藏的活动
                retdict = {}
                retdata=[]
                try:
                    favorites = self.db.query(Favorite).filter(Favorite.Fuid == user_id,Favorite.Ftype==2,
                                                               Favorite.Fvalid == 1).all()  # 返回收藏列表

                    #ap_favorates = []
                    for each_favorite in favorites:
                        ap_favorite_id = each_favorite.Ftypeid  # 即活动Id
                        print ap_favorite_id,'哈哈哈哈'
                        ap_favorite = self.db.query(Activity).filter(Activity.ACid == ap_favorite_id).one()
                        datauser=self.db.query(User).filter(User.Uid == user_id).one()
                        print datauser.Uid,'呵呵'
                        aclurl=self.db.query(ActivityImage).filter(ActivityImage.ACIacid==ap_favorite.ACid).limit(1).all()
                        #userurl=self.db.query(UserImage).filter(UserImage.UIuid == datauser.Uid).all()

                        user_headimages = self.db.query(UserImage).filter(
                            UserImage.UIuid == datauser.Uid).all()
                        userimg = []
                        for user_headimage in user_headimages:
                            exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                                 Image.IMvalid == 1).all()
                            if exist:
                                userimg = user_headimage
                                break;

                        ACFunction.Acresponse(ap_favorite,datauser,aclurl[0].ACIurl,userimg.UIurl,retdata,user_id)
                        print'哦哦哦'
                        #ap_favorates.append(ap_favorite)
                        #APmodelHandler.ap_Model_simply(ap_favorates, retdata, user_id)
                    self.retjson['code'] = '10551'
                    retdict['activity'] = retdata
                    self.retjson['contents'] = retdict
                except Exception, e:
                    print e
                    self.retjson['code'] = '10551'
                    self.retjson['contents'] = r''


        else:
            self.retjson['code'] = '10521'
            self.retjson['contents'] = r'用户认证错误！操作失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文

