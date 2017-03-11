# -*- coding: utf-8 -*-
'''
@author:王佳镭
@动态功能：用户收藏；取消收藏；查看所有收藏
'''
import json
import TRfunction
import Userinfo.Ufuncs
from BaseHandlerh import BaseHandler
from FileHandler.Upload import AuthKeyHandler
from Userinfo.Ufuncs import Ufuncs
from Database.tables import Trend, TrendImage, Image, Favorite


class TrendHandler(BaseHandler):
    retjson = {'code':'200','contents':'none'}

    def not_in_fav_list(self):
        self.retjson['code'] = '12030'
        self.retjson['contents'] = r"该用户未收藏此动态"
    def post(self):
        type = self.get_argument('type',default='null')
        u_id = self.get_argument('uid',default='null')
        auth_key =self.get_argument('authkey',default='null')
        ufunc = Userinfo.Ufuncs.Ufuncs()
        if ufunc.judge_user_valid(u_id,auth_key):
            if type == '12002' :#收藏动态
                trendid = self.get_argument('trendid',default='none')
                try:
                    exsit = self.db.query(Trend).filter(Trend.Tid==trendid).one()
                    print exsit.Tid
                    if exsit:
                        try:#判断是否已经有这行（即用户之前有没有操作过）
                            once_favorite = self.db.query(Favorite).filter(Favorite.Fuid == u_id , Favorite.Ftypeid == trendid ,Favorite.Ftype == 3).one()
                            print '哈哈哈'
                            print once_favorite.Fvalid
                            if once_favorite.Fvalid == 0 : #以前收藏过但取消了
                                once_favorite.Fvalid = 1  #重新收藏
                                exsit.TlikeN+=1
                                self.db.commit()
                                self.retjson['code']='12021'
                                self.retjson['contents']='收藏成功'
                            else:
                                self.retjson['code']='12022'
                                self.retjson['contents']='已经收藏过'
                        except Exception,e:#之前没有这行，没有收藏过
                            print e
                            new_favorite = Favorite(Fuid = u_id,
                                                    Ftype =3,
                                                    Ftypeid = trendid,
                                                    Fvalid =1
                                                    )
                            self.db.merge(new_favorite)
                            try:
                                exsit.TlikeN += 1
                                self.db.commit()
                                self.retjson['code']='12021'
                                self.retjson['contents']='收藏成功'
                            except Exception,e:
                                print e
                                self.retjson['contents']=r'操作数据库失败'
                except Exception,e:
                    print e
                    self.retjson['code']='12023'
                    self.retjson['contents']='该动态不存在'
            if type == '12003':  # 取消收藏动态
                trendid = self.get_argument('trendid')  # 动态id
                # todo：是否要判断该活动是否过期？
                try:
                    exsit = self.db.query(Trend).filter(Trend.Tid == trendid).one()
                    try:
                        once_favorite = self.db.query(Favorite).filter(Favorite.Ftype == 3, Favorite.Ftypeid == trendid,
                                                                       Favorite.Fuid == u_id).one()
                        if once_favorite.Fvalid == 1:  # 目前还在收藏夹中
                            try:
                                self.db.query(Favorite).filter(Favorite.Fuid == u_id, Favorite.Ftypeid == trendid). \
                                    update({Favorite.Fvalid: 0}, synchronize_session=False)
                                exsit.TlikeN -= 1
                                self.db.commit()
                                self.retjson['code'] = '12301'
                                self.retjson['contents'] = r'取消收藏动态成功'
                            except Exception, e:
                                print e
                                self.retjson['code']='12302'
                                self.retjson['contents'] = r'数据库提交失败'
                        else:  # 曾经收藏过，但是已经取消了
                            self.not_in_fav_list()
                    except Exception, e:
                        self.not_in_fav_list()
                except Exception, e:
                    self.not_in_fav_list()

            if type == '12004':  # 查看所有收藏的动态
                retdata = []
                try:
                    favorites = self.db.query(Favorite).filter(Favorite.Fuid == u_id,Favorite.Ftype==3,
                                                               Favorite.Fvalid == 1).all()  # 返回收藏列表
                    ap_favorates = []
                    exsit = 1
                    for each_favorite in favorites:

                        ap_favorite_id = each_favorite.Ftypeid  # 即动态Id
                        ap_favorite = self.db.query(Trend).filter(Trend.Tid == ap_favorite_id).one()
                        print '哈哈哈',ap_favorite.Tid
                        url = self.db.query(TrendImage).filter(TrendImage.TItid == ap_favorite.Tid).one()
                        TRfunction.TRresponse(ap_favorite,url.TIimgurl,retdata,exsit)
                    self.retjson['code'] = '12401'
                    self.retjson['contents'] = retdata
                except Exception, e:
                    print e
                    self.retjson['code'] = '12402'
                    self.retjson['contents'] = r'用户未收藏任何动态'


        else:
            self.retjson['code'] = '12403'
            self.retjson['contents'] = r'用户认证错误！操作失败'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))  # 返回中文





