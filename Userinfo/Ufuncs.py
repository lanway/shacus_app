#-*- coding:utf-8 -*-
'''
@author:黄鑫晨
#create_time:2016-09-01
'''
from Database.models import get_db
from Database.tables import User, AppointEntry, UserImage, Image
from FileHandler.Upload import AuthKeyHandler


class Ufuncs(object):
    #@staticmethod
    def get_user_id(self,u_auth_key):
        '''
        通过用户auth_key获得id
        :param u_auth_key:
        :return: 成功则返回id,失败返回0
        '''
        try:
            user = get_db().query(User).filter(User.Uauthkey == u_auth_key).one()

            uid = user.Uid
            print 'id from get auth key::;', uid
            return uid
        except Exception,e:
            print e
            return 0

    # @staticmethod
    # def user_auth():
    #@classmethod
    #@staticmethod
    def get_user_authkey(self,u_id):
        '''
        @attention: 直接调用时需要判断是否为0,返回0则该用户不存在
        :param self:
        :param u_id:
        :return:用户存在则返回u_auth_key，否则返回0
        '''
        try:
           user = get_db().query(User).filter(User.Uid == u_id).one()
           if user:
               u_auth_key = user.Uauthkey
               print 'authkey from id::;',u_auth_key
               return u_auth_key
        except Exception, e:
            print 'edsdsd:::',e
            return 0

    #@staticmethod
    def judge_user_valid(self, uid, u_authkey):
        #todo:可以完善区别是不合法还是用户不存在，以防止攻击
        '''
        判断用户是否合法
        :return:合法返回1，不合法返回0
        '''
        try:
            u_id = self.get_user_id(u_authkey)
            print 'id  from get user id::;', u_id
            if u_id == int(uid):
                return 1   # 合法
            else:
                print 'shdasidasd'
                return 0   # 不合法
        except Exception, e:
            print e
            return 0


    @staticmethod
    def get_userlist_from_ap(apid):
        '''
        Args:
            apid: 约拍id
        Returns:返回所有报名用户的用户简单模型

        '''
        users = []

        try:
            registers = get_db().query(AppointEntry).filter(AppointEntry.AEapid == apid,
                                                            AppointEntry.AEvalid == 1).all()  # 返回的是报名项
            for register in registers:
                user = {'id': '', 'headImage': ''}
                user['id'] = register.AEregisterID
                # todo: 待变为真图片
                #  user['uimgurl'] = get_db().query(UserImage.UIurl).filter(UserImage.UIuid == user['uid'])
                user['headImage'] = Ufuncs.get_user_headimage_intent_from_userid(user['id'])
                users.append(user)
            return users
        except Exception, e:
            print e


    @staticmethod
    def get_users_registlist_from_uids(userids):
        '''
        返回选择报名用户中用户详细模型
        Args:
            userids:
        Returns:
        '''
        users = []
        for userid in userids:
            try:
                user = get_db().query(User.Uid, User.Ualais, User.Usign).filter(User.Uid == userid).one()
                new_user = dict(
                    uid=user.Uid,
                    ualais=user.Ualais,
                    uimage=Ufuncs.get_user_headimage_intent_from_userid(user.Uid),
                    usign=user.Usign
                )
                users.append(new_user)
            except Exception, e:
                print e, "找用户出现错误"
        return users

    @staticmethod
    def get_users_chooselist_from_uids(userids, appointmentid):
        '''
        返回选择报名用户中用户详细模型
        Args:
            userids:
        Returns:
        '''
        users = []
        for userid in userids:
            try:
                register = get_db().query(AppointEntry.AEchoosed, AppointEntry.AEregisterID, AppointEntry.AEapid). \
                    filter(AppointEntry.AEapid == appointmentid, AppointEntry.AEregisterID == userid).one()
                user = get_db().query(User.Uid, User.Ualais, User.Usign).filter(User.Uid == userid).one()
                new_user = dict(
                    uid=user.Uid,
                    ualais=user.Ualais,
                    uimage=Ufuncs.get_user_headimage_intent_from_userid(user.Uid),
                    usign=user.Usign,
                    uchoosed=int(register.AEchoosed)
                )
                print '插入新用户'
                users.append(new_user)
            except Exception, e:
                print e, "找用户出现错误"
        return users


    @staticmethod
    def get_registids_from_appointment(appointment):
        userids = []
        try:
            #get_db().query(AppointEntry.AEregisterID).filter(appointment.APid == )
            apid = appointment.APid
            registids = get_db().query(AppointEntry.AEregisterID).filter(AppointEntry.AEapid == apid).all()
            for user in registids:
                userid = user.AEregisterID
                userids.append(userid)
        except Exception,e:
            print e
        return userids

    @staticmethod
    def get_user_headimage_intent_from_userid(userid):
        user_intent = ''
        authkey_handler = AuthKeyHandler()
        try:
            # user_images = get_db().query(UserImage).filter(UserImage.UIuid == userid).all()
            #user_image = get_db().query(UserImage).filter(UserImage.UIuid == userid).one()
            # user_images[0] = 'logo1.png'
            # for user_image in user_images:
            #     isvalid = get_db().query(Image).filter(Image.IMid == user_image.UIuid).one()
            #     if isvalid.IMvalie == 1:
            #         ui_url = user_image.UIurl
            user_headimages = get_db().query(UserImage).filter(UserImage.UIuid == userid).all()
            userimg = []
            for user_headimage in user_headimages:
                exist = get_db().query(Image).filter(Image.IMid == user_headimage.UIimid, Image.IMvalid == 1).all()
                if exist:
                    userimg = user_headimage
                    break;
            ui_url = userimg.UIurl
            user_intent = authkey_handler.download_url(ui_url)
            #         user_intent = authkey_handler.download_url(ui_url)
            #     else:
            #         user_intent = authkey_handler.download_url("logo1.png")
        except Exception, e:
            print e
            user_intent = authkey_handler.download_url("logo1.png")
        return user_intent








