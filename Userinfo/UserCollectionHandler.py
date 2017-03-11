# coding=utf-8
# 个人主页图片：包括个人照片和作品集
import json
import threading
from BaseHandlerh import BaseHandler
from Database.models import get_db
from Database.tables import User, UserHomepageimg, UserCollection, UClike, UCcomment
from FileHandler.Upload import AuthKeyHandler
from Userinfo.UserImgHandler import UserImgHandler


class UserCollectionHandler(BaseHandler):
    retjson = {'code': '', 'content': ""}
    def post(self):
        type = self.get_argument('type')

        # 作品集点赞/取消赞
        if type == '10840'or type == '10841':
            User_id = self.get_argument('uid')
            UC_id = self.get_argument('ucid')
            authkey = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()
                if userid:  # 验证通过
                    try:
                        User_Collection = self.db.query(UserCollection).filter(UserCollection.UCid == UC_id).one()
                        try:
                            once_liked = self.db.query(UClike).filter(UClike.UClikeUserid == User_id , UClike.UClikeid == UC_id).one()
                            if once_liked:   # 找到了对应的作品集
                                if once_liked.UCLvalid == 1:
                                    if type == '10840':  # 对作品集进行点赞
                                        self.retjson['code'] = '10842'
                                        self.retjson['content'] = r'已点过赞'
                                    elif type == '10841':  # 取消赞
                                        once_liked.UCLvalid = 0
                                        User_Collection.UClikeNum -= 1
                                        self.db.commit()
                                        self.retjson['code'] = '10842'
                                        self.retjson['content'] = r'取消赞成功'

                                else:  # 点过赞但是取消了once_liked.UCLvalid == 0
                                    if type == '10840':
                                        once_liked.UCLvalid = 1
                                        User_Collection.UClikeNum += 1
                                        self.db.commit()
                                        self.retjson['code'] = '10842'
                                        self.retjson['content'] = '点赞成功'
                                    elif type == '10841':
                                        self.retjson['code'] = '10842'
                                        self.retjson['content'] = r'用户已取消赞！'
                        # 没有找到类似点赞记录
                        except Exception, e:
                            print 'new like for a collection'
                            if type == '10841':
                                self.retjson['code'] = '10842'
                                self.retjson['content'] = r'用户未赞过此约拍！'
                            elif type == '10840':
                                new_UClike = UClike(
                                    UClikeid=UC_id,
                                    UCLvalid=1,
                                    UClikeUserid=User_id,
                                )
                                User_Collection.UClikeNum += 1
                                self.db.merge(new_UClike)
                                self.db.commit()
                                self.retjson['code'] = '10842'
                                self.retjson['content'] = '点赞成功'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '10843'
                        self.retjson['contents'] = '未找到此作品集'
                else:
                    print'认证错误'
                    self.retjson['code'] = '10813'
                    self.retjson['contents'] = '用户认证错误'
            except Exception, e:
                print e
                self.retjson['code'] = '10813'
                self.retjson['contents'] = '未找到该用户'
        # 添加作品集评论
        if type == '10844':
            User_id = self.get_argument('uid')
            UC_id = self.get_argument('ucid')
            authkey = self.get_argument('authkey')
            uc_comment = self.get_argument('comment')
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()
                if userid:  # 验证通过
                    try:
                        User_Collection = self.db.query(UserCollection).filter(UserCollection.UCid == UC_id).one()
                        new_UCcomment = UCcomment(
                            UCcommentid=UC_id,
                            UCcommentUserid=User_id,
                            UCcontent=uc_comment,
                        )
                        User_Collection.UCcommentNum += 1
                        self.db.merge(new_UCcomment)
                        self.db.commit()
                        self.retjson['code'] = '10844'
                        self.retjson['content'] = '评论成功'
                    except Exception, e:
                        print e
                        self.retjson['code'] = '10845'
                        self.retjson['content'] = '未找到此作品集'
                else:
                    print'认证错误'
                    self.retjson['code'] = '10845'
                    self.retjson['content'] = '用户认证错误'
            except Exception, e:
                print e
                self.retjson['code'] = '10845'
                self.retjson['content'] = '未找到该用户'


        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
