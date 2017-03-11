#-*- coding:utf-8 -*-
'''
@author:兰威
#create_time:2016-09-01
@type 用户关注请求
'''
import json

import Ufuncs
from BaseHandlerh import BaseHandler
from  Database.tables import UserLike, User, UCinfo, UserImage, Image
from FileHandler.Upload import AuthKeyHandler


class FindUlike(BaseHandler):

    #def __init__(self):
    retjson={'code' : '', 'contents': ''}

    '''
      处理用户互相关注

    '''

    def post(self):
        u_auth_key = self.get_argument('authkey')
        u_id = self.get_argument('uid')
        type = self.get_argument('type')
        ufuncs = Ufuncs.Ufuncs()
        if ufuncs.judge_user_valid(u_id, u_auth_key):
            if type == '10403':  #查询某人关注的人
                print '进入10403'
                see_id = self.get_argument('seeid')
                self.find_my_like(see_id)
            if type =='10401':   #关注某一人
                print '进入10401'
                followerID = self.get_argument("followerid")
                self.follow_user(u_id,followerID)
            if type =='10402': #取消关注某一人
                print '进入10402'
                followerID = self.get_argument("followerid")
                self.not_follow_user(u_id, followerID)
            if type =='10404':#c查询某人的粉丝
                print '进入10404'
                see_id =self.get_argument("seeid")

                self.find_my_follow(see_id)

        else:
            self.retjson['code'] = '10412'
            self.retjson['contents'] = '用户不合法'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 在当前目录下生成retjson文件输出中文


    def find_my_like(self, uid):
        '''
        查询所有我关注的人
        :param uid:‘我的’Id
        :return:
        '''
        retdata = []
        try:
            my_likes = self.db.query(UserLike).filter(UserLike.ULlikeid == uid,UserLike.ULvalid,UserLike.ULvalid == 1).all()
            print '进入10403查询'
            if my_likes:

                for my_like in my_likes:

                    my_like_id = my_like.ULlikedid
                    userinfo = self.db.query(User).filter(User.Uid == my_like_id).one()
                    auth = AuthKeyHandler()
                    user_headimages = self.db.query(UserImage).filter(UserImage.UIuid == my_like_id).all()
                    userimg = []
                    for user_headimage in user_headimages:
                        exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                             Image.IMvalid == 1).all()
                        if exist:
                            userimg = user_headimage
                            break;
                    user_json = {'uid': userinfo.Uid, 'ualais': userinfo.Ualais, 'usign': userinfo.Usign,
                                 'uimgurl': auth.download_url(userimg.UIurl)}
                    retdata.append(user_json)
                    print '成功返回关注者'
                    self.retjson['code'] = '10430'
                    self.retjson['contents'] = retdata
            else:
                print "没有关注任何人"
                self.retjson['code'] = '10431'
                self.retjson['contents'] = r'该用户没有关注任何人'
        except Exception,e:
            self.retjson['code'] = '10431'
            self.retjson['contents'] = r'该用户没有关注任何人'




    def follow_user(self,u_id,follower_id):
            try:
                exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                           UserLike.ULlikedid == follower_id,
                                                       ).one()
                if exist.ULvalid == True:
                        self.retjson['code'] = '10410'
                        self.retjson['contents'] = '您已经关注过该用户'
                else :
                    exist.ULvalid =True
                    my = self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
                    my.UClikeN += 1
                    follower = self.db.query(UCinfo).filter(UCinfo.UCuid == follower_id).one()
                    follower.UClikedN += 1
                    self.db.commit()
                    self.retjson['code'] = '10411'
                    self.retjson['contents'] = '关注成功'
            except Exception, e:
                    print '开始关注该用户'
                    new_userlike = UserLike(
                        ULlikeid=u_id,
                        ULlikedid=follower_id,
                        ULvalid=1
                         )
                    self.db.merge(new_userlike)
                    my = self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
                    my.UClikeN += 1
                    follower = self.db.query(UCinfo).filter(UCinfo.UCuid == follower_id).one()
                    follower.UClikedN += 1
                    try:
                        self.db.commit()
                        self.retjson['code'] = '10411'
                        self.retjson['contents'] = '关注成功'
                    except Exception, e:
                        print e
                        self.db.rollback()
                        self.retjson['code'] = '10419'
                        self.retjson['contents'] = '服务器错误'

    def not_follow_user(self,u_id,follower_id):
        try:
            exist = self.db.query(UserLike).filter(UserLike.ULlikeid == u_id,
                                                   UserLike.ULlikedid == follower_id,
                                                   UserLike.ULvalid == True).one()
            if exist:
                exist.ULvalid = 0
                my = self.db.query(UCinfo).filter(UCinfo.UCuid == u_id).one()
                my.UClikeN -= 1
                follower = self.db.query(UCinfo).filter(UCinfo.UCuid == follower_id).one()
                follower.UClikedN -= 1
                try:
                    self.db.commit()
                    self.retjson['contents'] = '取消关注成功'
                    self.retjson['code'] = '10420'
                except Exception,e :
                    print e
                    self.db.rollback()
                    self.retjson['code'] = '10419'
                    self.retjson['contents'] = '服务器错误'
        except Exception,e :
            print e
            self.retjson['contents'] = '未关注该用户'
            self.retjson['code'] = '10421'

    def find_my_follow(self, uid):
        retdata = []
        try:
            my_likes = self.db.query(UserLike).filter(UserLike.ULlikedid == uid,UserLike.ULvalid == 1).all()
            print '进入10404查询'
            if my_likes:

                for my_like in my_likes:

                    my_like_id = my_like.ULlikeid
                    auth = AuthKeyHandler()
                    user_headimages = self.db.query(UserImage).filter(UserImage.UIuid == my_like_id).all()
                    userimg = []
                    for user_headimage in user_headimages:
                        exist = self.db.query(Image).filter(Image.IMid == user_headimage.UIimid,
                                                            Image.IMvalid == 1).all()
                        if exist:
                            userimg = user_headimage
                            break;
                    userinfo = self.db.query(User).filter(User.Uid == my_like_id,).one()
                    #接来下测试是否我也关注了我的粉丝
                    try:
                       exist = self.db.query(UserLike).filter(UserLike.ULlikedid == my_like_id,
                                                           UserLike.ULlikeid == uid,
                                                              UserLike.ULvalid == True).one()
                       if exist :
                        text =True
                    except Exception,e:
                        text=False
                    user_json = {'uid': userinfo.Uid, 'ualais': userinfo.Ualais, 'usign': userinfo.Usign,
                                 'uimgurl':auth.download_url(userimg.UIurl) ,'fansback':text}
                    retdata.append(user_json)
                print '成功返回粉丝'
                self.retjson['code'] = '10440'
                self.retjson['contents'] = retdata
            else:
                print '886'
                self.retjson['code'] = '10441'
                self.retjson['contents'] = r'你是没有人关注的'
        except Exception,e:
            print 'gdfgdfgdfg',e
            self.retjson['code'] = '10441'
            self.retjson['contents'] = r'你是没有人关注的'

