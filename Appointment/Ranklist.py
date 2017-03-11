# coding=utf-8
'''
@author:黄鑫晨
@create_time:2016-09-09
'''
import json
from Database.models import get_db
from sqlalchemy import desc

from BaseHandlerh import BaseHandler
from Database.tables import User, RankScore, AppointmentInfo
from Userinfo import Usermodel
from Userinfo.Ufuncs import Ufuncs
from FileHandler.Upload import AuthKeyHandler

global db
db = get_db()

# 排行榜共有多少名
global last
# 目前排行榜共有十名
last = 10
class Ranklist(BaseHandler):
    '''
        用来与客户端通信的类
    '''
    retjson = {'code':'10287', "content": '意外错误'}
    def post(self):
        type = self.get_argument('type')
        u_auth_key = self.get_argument('authkey')
        uid = self.get_argument('uid')
        rank_list_handler = RanklistHandler()
        ufunc = Ufuncs()
        if ufunc.judge_user_valid(uid, u_auth_key):  # 用户验证成功
            if type == '10281':  # 请求摄影师排行get_rank_photoers
                self.retjson['content'] = rank_list_handler.get_rank_photoers()
                self.retjson['code'] = '10285'
            elif type == '10282':  # 请求模特排行
                self.retjson['code'] = '10285'
                self.retjson['content'] = rank_list_handler.get_rank_models()
        else:
            self.retjson['code'] = '10286'
            self.retjson['content'] = u'用户认证失败！'
        self.write(json.dumps(self.retjson, ensure_ascii=False, indent=2))
    def get(self):
        rlhandler = RanklistHandler()
        rlhandler.rank_model_init()
        rlhandler.rank_photoer_init()


class RanklistHandler(object):
    retjson = {'code': '', "content": ''}
    '''
        用来处理排行榜的计算的类
    '''
    def get_model_list(self):
        '''
        获取模特排行榜前十的RankScore模型
        Returns:获得前十模特的RankScore模型
        '''
        try:
            models = db.query(RankScore).filter(RankScore.RSMrank<=last).all()   # 排行榜前十的模特
            return models
        except Exception, e:
            print e, u'获取排行榜列表时出现异常'
            # self.retjson['code'] = '10286'
            # self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_photoer_list(self):
        '''
        获取摄影师排行榜前十的RankScore模型
        Returns:前十摄影师的RankScore模型
        '''
        try:
            photoers = db.query(RankScore).filter(RankScore.RSPrank<=last).all()  # 排行榜前十的摄影师
            return photoers
        except Exception, e:
            print e, u'获取排行榜列表时出现异常'
            # self.retjson['code'] = '10286'
            # self.retjson['content'] = u'获取排行榜列表时出现异常'

    def get_rank_photoers(self):
        '''
        Returns:获得前十名摄影师的用户模型
        '''
        photoers_user_models = self.get_rank_list_usermodel(self.get_photoer_list(), 1)  # 前十摄影师的用户模型
        return photoers_user_models

    def get_rank_models(self):
        '''
        Returns:得前十名模特的用户模型
        '''
        models_user_models = self.get_rank_list_usermodel(self.get_model_list(), 2)  # 前十模特的用户模型
        return  models_user_models


    def get_rank_list_usermodel(self, rs_models, type):
        '''
        Args:
            type: 1为摄影师，2为模特
            rs_models: 排行榜摄影师或模特的RankScore模型
        Returns:排行榜摄影师的用户模型
        '''
        user_models = []
        auth = AuthKeyHandler()
        for rs_umodel in rs_models:
            rs_u_id = rs_umodel.RSuid  # 摄影师的用户id
            try:
                user = db.query(User).filter(User.Uid == rs_u_id).one()
                user_model = Usermodel.get_user_detail_from_user(user)
                # 摄影师
                if type == 1:
                    user_model['rank'] = rs_umodel.RSPrank
                    user_model['image'] =auth.download_url('0'+str(user.Uid)+'.png')
                    #print user_model.id
                # 模特
                elif type == 2:
                    user_model['rank'] = rs_umodel.RSMrank
                    user_model['image'] = auth.download_url(str(user.Uid) + '.png')
                user_models.append(user_model)

            except Exception, e:
                print e, u"未查找找到该用户"
                # self.retjson['code'] = '10285'
                # self.retjson['content'] = u"未查找找到该用户"
        return user_models


    def insert_new_rank(self,userid):
        '''
        用户初始化时，添加入新的排行榜
        Args:
            userid: 用户id
        Returns:
        '''
        try:
            rank_user = db.query(RankScore).filter(RankScore.RSuid == userid).one()
            if rank_user:
                print "该用户已初始化过！"
        except Exception, e:
            print e
            new_rs = RankScore(
                RSuid=userid,
                RSMscore=0,
                RSPscore=0,
                RSMrank=101,
                RSPrank=101
                )
            try:

                db.merge(new_rs)
                db.commit()
            except Exception, e:
                print e

    def rank_judge_photoer_up(self, rs_p):
        '''
        每次排行榜分数变动后，此方法对此次变动的模特的分数与排行榜进行比较，
        判断是否能进入排行榜
        如果进入则冒泡排序，升降名次
        在约拍结束等加分项后调用
        Args:
            rs_p: 摄影师的RankScore表项
        Returns:
            将rs_p的RSPscore与前面的RSPscore比较
        '''

        p_score = rs_p.RSPscore

        # 如果此模特分数增加后比排行榜最末端高：
        if p_score > self.get_modellist_some_score(last):
            # compareN: 每次比较的名次
            # 冒泡排序
            # 临时名次
            temp_rank = last
            compare_rank = last
            compare_rank -= 1
            # 当前的分数大于前一名的分数
            while compare_rank >= 1 and p_score > self.get_photoerlist_some_score(compare_rank) :
                #自己的名次等于前一名的名次
                rs_p.RSPrank = compare_rank
                #前一名的名次后退一步
                formor_model = self.get_photoerlist_some(compare_rank)
                formor_model.RSPrank += 1
                db.commit()






    def rank_score_finish_appoint(self, appointinfo):
        '''
        此为完成一次约拍后，模特与摄影师加分
        @attention：注意是加分，减分在其他函数中
        加分规则：
        1.完成后，摄影师、模特直接加分
        2.按照对方评分（满意度），再增添相应积分
        Args:
            userid: 用户id
            type: 用户在此约拍中类型，1为摄影师，2为模特
            appointment:AppointInfo的一列

        Returns:直接加分，不用

        '''
        uid_model = appointinfo.AImid
        uid_photoer = appointinfo.AIpid


        try:
            # 模特项
            rs_model = db.query(RankScore.RSuid, RankScore.RSMscore, RankScore.RSid).\
                filter(RankScore.RSuid == uid_model).one()
            # 模特加分
            score = RankScore.RSMscore + 10
            db.query(RankScore).filter(RankScore.RSuid == rs_model.RSuid).\
                update({RankScore.RSMscore: score})
            # todo：排名上升下降


            # 摄影师项
            rs_photoer = db.query(RankScore.RSuid, RankScore.RSMscore, RankScore.RSid).filter(
                RankScore.RSuid == uid_photoer).one()
            score = RankScore.RSPscore + 10
            db.query(RankScore).filter(RankScore.RSuid == rs_photoer.RSuid).\
                update({RankScore.RSPscore: score})
            #摄影师加分
            # todo：排名上升下降
            db.commit()
        except Exception, e:
            print e, "排行榜查询错误1"

    def get_modellist_some_score(self, rank):
        '''
        @rank:名次
        Returns: 得到模特榜某一名的分数的分数
        '''
        try:
            # 模特榜最后一名
            model_last = db.query(RankScore.RSMrank, RankScore.RSMscore).filter(RankScore.RSMrank == rank).one()
            return model_last.RSMscore
        except Exception, e:
            print e, "读取模特榜某一名时出错"

    def get_photoerlist_some_score(self, rank):
        '''
        @rank:名次
        Returns: 得到摄影师榜某一名的分数
        '''
        try:
            # 摄影师榜最后一名
            photoer_one = db.query(RankScore.RSMrank, RankScore.RSMscore).filter(RankScore.RSMrank == rank).one()
            return photoer_one.RSMscore
        except Exception, e:
            print e, "读取摄影师榜某一名时出错"

    def get_photoerlist_some(self, rank):
        '''
        @rank:名次
        Returns: 得到摄影师榜某一名的项
        '''
        try:
            # 摄影师榜最后一名
            photoer_one = db.query(RankScore.RSMrank, RankScore.RSMscore).filter(RankScore.RSMrank == rank).one()
            return photoer_one
        except Exception, e:
            print e, "读取摄影师榜某一名时出错"

    def rank_model_init(self):
        '''
        对模特榜进行排序
        '''
        try:
            models = db.query(RankScore.RSMrank, RankScore.RSMscore, RankScore.RSuid).order_by(desc(RankScore.RSMscore)).all()
            rank = 1
            for model in models:
                db.query(RankScore).filter(RankScore.RSuid == model.RSuid).update({RankScore.RSMrank: rank})
                rank += 1
            db.commit()
        except Exception, e:
            print e, "对模特榜进行排序时出错！"

    def rank_photoer_init(self):
        '''
        对摄影师榜进行排序
        '''
        try:
            models = db.query(RankScore.RSPrank, RankScore.RSPscore, RankScore.RSuid).order_by(desc(RankScore.RSPscore)).all()
            rank = 1
            for model in models:
                db.query(RankScore).filter(RankScore.RSuid == model.RSuid).update({RankScore.RSPrank: rank})
                rank += 1
            db.commit()
        except Exception, e:
            print e, "对模特榜进行排序时出错！"





#apinfo = db.query(AppointmentInfo).filter(AppointmentInfo.AIappoid == 24).one()
#rlhandler.rank_score_finish_appoint(apinfo)
