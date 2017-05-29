# coding=utf-8
import time

from Database.models import get_db
from Database.tables import UserImage, Image, User, UserCollectionimg, UserCollection
from FileHandler.ImageHandler import ImageHandler
from FileHandler.Upload import AuthKeyHandler
from Database.models import get_db
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
'''
@author: 黄鑫晨 兰威
'''

def userinfo_smply(u_info, u_change_info):
    '''

    Args:
        u_info:
        u_change_info:
    返回个人简单信息
    Returns:

    '''
    auth = AuthKeyHandler()
    user_headimages = get_db().query(UserImage).filter(UserImage.UIuid == u_info.Uid).all()
    userimg = []
    for user_headimage in user_headimages:
        exist = get_db().query(Image).filter(Image.IMid == user_headimage.UIimid, Image.IMvalid == 1).all()
        if exist:
            userimg = user_headimage
            break
    ret_info = {'uid': u_info.Uid, 'ualais': u_info.Ualais, 'ulocation': u_info.Ulocation,
                     'utel': u_info.Utel, 'uname': u_info.Uname, 'umailbox': u_info.Umailbox,
                     'ubirthday': u_info.Ubirthday.strftime('%Y-%m-%d %H:%M:%S'), 'uscore': u_info.Uscore, 'usex': u_info.Usex,
                     'usign': u_info.Usign, 'uimage': auth.download_assign_url(userimg.UIurl, 200, 200), 'ulikeN': u_change_info.UClikeN,
                     'ulikedN': u_change_info.UClikedN, 'uapN': u_change_info.UCapN,
                     'uphotoN': u_change_info.UCphotoN, 'ucourseN': u_change_info.UCcourseN,
                     'umomentN': u_change_info.UCmomentN}
    return ret_info

def Model_daohanglan(imgurl,weburl):
    dh_json = {'imgurl':imgurl, 'weburl':weburl}
    return dh_json

def user_login_fail_model():
    user_model = dict(
        id='0',
        phone='wu',
        nickName='wu',
        realName='wu',
        sign='wu',
        sex='wu',
        score='wu',
        location='wu',
        birthday='wu',
        registTime='wu',
        mailBox='wu',
        headImage='wu',
        auth_key='wu'
    )
    return user_model

def get_user_detail_from_user(user):
    # try:
    #     if user.Ubirthday:
    #         Ubirthday = user.Ubirthday.strftime('%Y-%m-%d %H:%M:%S'),
    #     else:
    #         Ubirthday = ''
    # except Exception, e:
    #     print e
    #     Ubirthday = ''
    if user.Usex == True:
        gender = 1
    else:
        gender = 0
    user_model = dict(
        id=user.Uid,
        phone=user.Utel,
        nickName=user.Ualais,
        realName=user.Uname,
        sign=user.Usign,
        sex=gender,
        score=user.Uscore,
        location=user.Ulocation,
        birthday=user.Ubirthday.strftime('%Y-%m-%d'),
        registTime=user.UregistT.strftime('%Y-%m-%d %H:%M:%S'),
        mailBox=user.Umailbox,
        headImage=Ufuncs.get_user_headimage_intent_from_userid(user.Uid),
        auth_key=user.Uauthkey,
        chattoken=user.Uchattoken
    )
    return user_model

# 推荐摄影师模特列表
def rec_user_list(user):
    # user是一个用户模型而且必须有作品集
    try:
        imghandler= AuthKeyHandler()
        uhead_pic = get_db().query(UserImage).filter(UserImage.UIuid == user.Uid).all()
        # 该用户的所有作品集
        uc_list = get_db().query(UserCollection).filter(UserCollection.UCuser == user.Uid).all()
        # 用户第一个作品集所有图片
        print uc_list[0].UCid
        uc_pic = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == uc_list[0].UCid).all()

        piclist = []
        uc_all_pic = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == uc_list[0].UCid).limit(5).all()
        for item in uc_all_pic:
            piclist.append(imghandler.download_url(item.UCIurl))
        user_bir = user.Ubirthday.strftime('%Y')  # 获取用户生日（年）
        now = time.strftime('%Y', time.localtime(time.time()))  # 获取当前年份
        user_age = int(now) - int(user_bir)  # 用户年龄
        usermodel = dict(
            id=user.Uid,  # 用户id
            phone=user.Utel,  # 用户手机号
            nickName=user.Ualais,  # 用户名
            age=user_age,  # 用户年龄
            sex=int(user.Usex),  # 用户性别
            Ucategory=user.Ucategory,    # 用户类型
        )
        user_model = dict(
            userpublish=usermodel,
            headimg=imghandler.download_url(uhead_pic[-1].UIurl),      # 用户头像
            UcFirstimg=imghandler.download_originpic_url(uc_pic[0].UCIurl),          # 作品集第一张
            Ucimg=piclist,
        )
        return user_model
    except Exception, e:
        print e
        # print '推荐列表没有获取到用户'


