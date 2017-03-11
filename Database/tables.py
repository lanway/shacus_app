# -*- coding: utf-8 -*-


'''
@author: 黄鑫晨 兰威 王佳镭
'''

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData,ForeignKey,DateTime,Boolean
from sqlalchemy.types import CHAR, Integer, VARCHAR,Boolean,Float
from sqlalchemy.sql.functions import func
from models import Base
import sys
reload(sys)

# from models import engine

# 每个类对应一个表
class User(Base): # 用户表   #添加聊天专用chattoken
    __tablename__ = 'User'

    Uid = Column(Integer, nullable=False, primary_key=True)  # 主键
    Upassword = Column(VARCHAR(16), nullable=False)
    Utel = Column(CHAR(11),nullable=False,unique=True,)
    Ualais = Column(VARCHAR(24),nullable=False,unique=True) # 昵称
    Uname = Column(VARCHAR(24),nullable=True) # 真实姓名
    Ulocation = Column(VARCHAR(128))
    Umailbox = Column(VARCHAR(32))#unique=True) # unique表示唯一性
    Ubirthday = Column(DateTime)
    Uscore = Column(Integer, default=0)
    UregistT = Column(DateTime(timezone=True), default=func.now())
    Usex = Column(Boolean,nullable=False)
    Usign = Column(VARCHAR(256))
    Uauthkey = Column(VARCHAR(32))
    Uchattoken = Column(VARCHAR(128), nullable=False)

class UCinfo(Base):
    __tablename__ = 'UCinfo'

    UCuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'),nullable=False,primary_key=True)
    UClikeN = Column(Integer, nullable=False, default=0)
    UClikedN = Column(Integer, nullable=False, default=0)
    UCapN = Column(Integer, nullable=False, default=0)
    UCphotoN = Column(Integer, nullable=False, default=0)
    UCcourseN = Column(Integer, nullable=False, default=0)
    UCmomentN = Column(Integer, nullable=False, default=0)

class Verification(Base): # 短信验证码及生成用户auth_key时间
    __tablename__ = 'Verification'

    Vphone = Column(CHAR(11),primary_key=True) #
    Vcode = Column(CHAR(6),nullable=False)
    VT = Column(DateTime(timezone=True), default=func.now()) # 待测试是插入数据的时间还是最后一次更新该表的时间 （测试结果为第一次插入时间）

class Activity(Base):#活动表
    __tablename__ = 'Activity'

    ACid = Column(Integer,nullable=False, primary_key=True)
    ACsponsorid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))  #活动发起者
    AClocation = Column(VARCHAR(128), nullable=False)
    ACtitle = Column(VARCHAR(24), nullable=False) # 活动的名称？确认长度
    ACtag = Column(VARCHAR(12)) # 活动的标签？确认类型
    ACstartT = Column(DateTime, nullable=False)
    ACendT = Column(DateTime, nullable=False)
    ACjoinT = Column(DateTime) # 活动报名截止时间
    ACcontent = Column(VARCHAR(128), nullable=False) # 活动介绍
    ACfree = Column(Boolean)
    ACprice = Column(VARCHAR(64))
    ACclosed = Column(Boolean,default=1, nullable=False) # 活动是否已经结束
    ACcreateT = Column(DateTime(timezone=True), default=func.now())
    ACcommentnumber = Column(Integer,default=0, nullable=False)
    ACmaxp = Column(Integer,nullable=False,default=0)
    ACminp = Column(Integer,nullable=False,default=100)
    ACscore = Column(Integer,nullable=False,default=0)
    AClikenumber = Column(Integer,nullable=False,default=0)
    ACvalid = Column(Boolean,nullable=False,default=1) # 活动是否已经删除
    ACregistN = Column(Integer,nullable=False,default=0)
    ACstatus =Column(Integer,nullable=False,default=0)


class ActivityEntry(Base):  #活动报名表
    __tablename__ = 'Activityaentry'

    ACEid=Column(Integer,primary_key=True)
    ACEacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))  # 活动ID
    ACEregisterid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))  # 报名人ID
    ACEregisttvilid = Column(Boolean,default=1)
    ACEscore = Column(Integer,nullable=False,default=0)
    ACEcomment = Column(VARCHAR(128),nullable=False,default='')
    ACEregisterT = Column(DateTime(timezone=True), default=func.now())

class ActivityLike(Base):
    __tablename__ = 'ActivityLike'

    ACLid=Column(Integer,primary_key=True)
    ACLacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACLuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'))
    ACLvalid = Column(Boolean,nullable=False,default=1)
    ACLT = Column(DateTime, default=func.now())

class CheckIn(Base):
    __tablename__ = 'CheckIn'

    # 复合主键
    CLuid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),primary_key=True)
    CLcheckday = Column(DateTime(timezone=True), default=func.now())


class UserLike(Base):
    __tablename__ = 'UserLike'

    ULid=Column(Integer,primary_key=True,nullable=False)
    ULlikeid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),nullable=False)
    ULlikedid = Column(Integer,ForeignKey('User.Uid',onupdate='CASCADE'),nullable=False)
    ULvalid = Column(Boolean, nullable= False, default=1)
    ULlikeT = Column(DateTime(timezone=True), default=func.now())

class Image(Base):
    __tablename__ = 'Image'

    IMid = Column(Integer,primary_key=True,nullable=False)
    IMvalid = Column(Boolean,default=1)
    IMT = Column(DateTime(timezone=True), default=func.now())
    IMname = Column(VARCHAR(128), nullable=False)

class ActivityImage(Base):
    __tablename__ = "ActivityImage"

    ACIacid = Column(Integer,ForeignKey('Activity.ACid',onupdate='CASCADE'))
    ACIimid = Column(Integer,ForeignKey('Image.IMid',onupdate='CASCADE'),primary_key=True)
    ACIurl = Column(VARCHAR(128))#数据长度

class AppointmentImage(Base):
    __tablename__ = 'AppointImage'

    APIapid = Column(Integer,ForeignKey("Appointment.APid",onupdate="CASCADE"))
    APIimid = Column(Integer,ForeignKey("Image.IMid",onupdate="CASCADE"),primary_key=True)
    APIurl = Column(VARCHAR(128))

class UserImage(Base):
    __tablename__ = 'UserImage'

    UIuid = Column(Integer,ForeignKey("User.Uid", onupdate="CASCADE"))
    UIimid = Column(Integer,ForeignKey("Image.IMid", onupdate="CASCADE"), primary_key=True)
    UIurl = Column(VARCHAR(128))

class Appointment(Base):  #摄影师-模特约拍
    __tablename__ = 'Appointment'

    APid = Column(Integer, primary_key=True, nullable=False)
    APsponsorid = Column(Integer, ForeignKey('User.Uid', ondelete='CASCADE'), nullable=False)  # 发起者
    APtitle=Column(VARCHAR(24),nullable=False)
    APlocation = Column(VARCHAR(128), nullable=False)
    APtag=Column(VARCHAR(12)) # 约拍标签？确认长度
    APstartT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APendT = Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APjoinT=Column(DateTime, nullable=False, default='0000-00-00 00:00:00 ')
    APcontent=Column(VARCHAR(128), nullable=False, default='')
    APfree = Column(Boolean)
    APprice = Column(VARCHAR(64))
    APclosed = Column(Boolean)
    APcreateT = Column(DateTime(timezone=True), default=func.now())
    APtype = Column(Boolean,nullable=False,default=0) # 约拍类型，模特约摄影师(1)或摄影师约模特(0)
    APaddallowed = Column(Boolean,default=0)
    APlikeN = Column(Integer, default=0, nullable=False)
    APvalid = Column(Boolean, default=1, nullable=False)
    APregistN = Column(Integer, nullable=False, default=0)
    APstatus = Column(Integer, nullable=False, default=0)
    APgroup = Column(Integer, nullable=False, default=0)


class AppointmentInfo(Base):
    __tablename__ = "Appointmentinfo"

    AIid = Column(Integer,primary_key=True)
    AImid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))
    AIpid = Column(Integer,ForeignKey('User.Uid', ondelete='CASCADE'))
    AImscore = Column(Integer,default=0)
    AIpscore = Column(Integer,default=0)
    AImcomment = Column(VARCHAR(128))
    AIpcomment = Column(VARCHAR(128))
    AIappoid = Column(Integer,ForeignKey('Appointment.APid',onupdate='CASCADE'))#与AIid相同，是否重复？

class AppointEntry(Base):
    __tablename__ = "AppointEntry"

    AEapid=Column(Integer, ForeignKey('Appointment.APid' ,onupdate="CASCADE") )
    AEid = Column(Integer, primary_key=True)
    AEapid = Column(Integer, ForeignKey('Appointment.APid',onupdate='CASCADE'))
    AEregisterID = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    AEvalid = Column(Boolean, nullable=False,default=1)
    AEchoosed = Column(Boolean, nullable=False,default=0)
    AEregistT = Column(DateTime(timezone=True), default=func.now())


class AppointLike(Base):
    __tablename__ = 'AppointLike'

    ALid=Column(Integer,primary_key=True)
    ALapid = Column(Integer,ForeignKey('Appointment.APid',onupdate='CASCADE'))
    ALuid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'))
    ALvalid = Column(Boolean,nullable=False, default=1)
    ALT = Column(DateTime(timezone=True), default=func.now())

class Favorite(Base):
    __tablename__ = 'Favorite'

    Fid = Column(Integer, primary_key=True)
    Fuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'), nullable=False)
    Ftype = Column(Integer, nullable=False, default=0)   # 1为约拍，2为
    Ftypeid = Column(Integer, nullable=False, default=0)
    FT = Column(DateTime(timezone=True), default=func.now())
    Fvalid = Column(Boolean, nullable=False, default=1)

class  Course(Base):   #教程数据库
    __tablename__ = "Course"

    Cid = Column(Integer,primary_key=True)
    Curl = Column(VARCHAR(128),nullable= False)
    ClikeN = Column(Integer,nullable= False,default= 0)
    CwatchN = Column(Integer,nullable= False,default=0)
    CfavN = Column(Integer,nullable=False,default=0)
    Cscore = Column(Integer,nullable= False,default=0)
    Ctype = Column(Integer,nullable= False)
    Cvalid =Column(Integer,nullable= False,default= 0)
    Csponsorid = Column(Integer,nullable=False)
    Cimagerul = Column(VARCHAR(128),nullable= False)
    Ctitle = Column(VARCHAR(32),nullable= False)

class CourseTag(Base): #教程标签类型
    __tablename__ = 'CourseTag'

    CTid = Column(Integer,nullable= False,primary_key=True)
    CTname = Column(VARCHAR(32), nullable=False)
    CThint = Column(VARCHAR(128), nullable=False)
    CTcourseN = Column(Integer,nullable=False,default= 0)
    CTimageurl = Column(VARCHAR(128),nullable=False)
    CTvalid = Column(Boolean ,nullable=False,default= 0)

class CourseTagEntry(Base):  #课程与标签联系的表
    __tablename__="CourseTagEntry"

    CTEcid = Column(Integer,ForeignKey('Course.Cid', onupdate='CASCADE'),nullable=False,primary_key=True)
    CTEtid = Column(Integer,ForeignKey('CourseTag.CTid',onupdate='CASCADE'),nullable=False,primary_key=True)
    CTEvalid = Column(Boolean,nullable=False,default= 0)
    CTEcreateT = Column(DateTime(timezone=True), default=func.now())

class CourseLike(Base):  #课程点赞表
    __tablename__ = "CourseLike"

    CLcid = Column(Integer,ForeignKey('Course.Cid', onupdate='CASCADE'),primary_key=True)
    CLuid = Column(Integer,ForeignKey('User.Uid', onupdate='CASCADE'),primary_key=True)
    CLlikeT = Column(DateTime(timezone=True), default=func.now())
    CLvalid = Column(Boolean,nullable=False,default=0)

class Usercourse(Base):   #和用户有关的教程
    __tablename__ = "Usercourse"

    UCuid = Column(Integer, ForeignKey('User.Uid',onupdate='CASCADE'),primary_key=True)
    UCcid = Column(Integer, ForeignKey('Course.Cid',onupdate='CASCADE'),primary_key=True)
    UCseen = Column(Boolean,nullable=False,default=0)
    UCfav = Column(Boolean,nullable=False,default=0)

class Trend(Base):
    __tablename__ = "Trend"

    Tid = Column(Integer, primary_key=True)
    Tsponsorimg = Column(VARCHAR(128),nullable=False)
    Tsponsorid = Column(Integer, ForeignKey('User.Uid',onupdate='CASCADE'),primary_key=True)  #用户id
    TsponsT = Column(DateTime(timezone=True), default=func.now())                                         #时间
    TcommentN = Column(Integer,nullable=False, default=0)
    TlikeN =Column(Integer,nullable=False, default=0)
    Tcontent = Column(VARCHAR(128), nullable=False)
    Ttitle = Column(VARCHAR(12), nullable=False)

class TrendImage(Base):
    __tablename__ = 'TrendImage'
    TIid = Column(Integer ,primary_key=True)
    TItid =Column (Integer,ForeignKey('Trend.Tid',onupdate='CASCADE'),primary_key=True)
    TIimid = Column(Integer,ForeignKey('Image.IMid',onupdate='CASCADE'),primary_key=True)
    TIimgurl = Column(VARCHAR(128))


class RankScore(Base):
    '''
       摄影师模特排行榜
       每个用户仅能有一列
       @RSMscore:用户在当模特方面的分数
       @RSPscore：用户在当摄影师方面的分数
    '''
    __tablename__ = 'RankScore'
    RSid = Column(Integer, nullable=False, primary_key=True)
    RSuid = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'), nullable=False)
    RSMscore = Column(Integer, nullable=False, default=0)
    RSPscore = Column(Integer, nullable=False, default=0)
    RSMrank = Column(Integer, nullable=False, default=101)
    RSPrank = Column(Integer, nullable=False, default=101)

class WeAcToken(Base):
    '''
    用于存放微信accesstoken
    '''
    __tablename__ = 'WeAcToken'
    WACid = Column(Integer,primary_key=True)
    WACtoken = Column(VARCHAR(512))
    WACexpire = Column(Integer,nullable=False,default=0)

class UserHomepageimg(Base):
    #用户个人图片展示
    __tablename__ = 'UserHomepageimg'
    UHpageid= Column(Integer, primary_key=True)
    UHuser = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'))
    UHimgid = Column (Integer, ForeignKey('Image.IMid', onupdate='CASCADE'))
    UHpicurl= Column(VARCHAR(128))
    UHpicvalid = Column(Integer, default=0)
    UHheight = Column(Integer,default=0)
    UHwidth = Column(Integer,default=0)

class UserCollection(Base):
    #用户作品集
    __tablename__ = 'UserCollection'
    UCid = Column(Integer, primary_key=True,nullable=False)
    UCuser = Column(Integer, ForeignKey('User.Uid', onupdate='CASCADE'),nullable=False)
    UCcreateT = Column(DateTime(timezone=True), default=func.now())
    UCtitle = Column(VARCHAR(32), nullable=False)  #作品集名称
    UCcontent = Column(VARCHAR(128))               #作品集描述
    UCvalid = Column(Integer, default=0)
    UCiscollection = Column(Integer, default=0) #0是作品集 1是动态
    UClikeNum = Column(Integer, default=0)
    UCcommentNum = Column(Integer, default=0)

class UserCollectionimg(Base):
    __tablename__ = 'UserCollectionimg'
    UCIuser = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE')) #作品集id
    UCIimid = Column(Integer, ForeignKey(Image.IMid, onupdate='CASCADE'), primary_key=True)
    UCIurl = Column(VARCHAR(128))
    UCIvalid = Column(Integer, nullable=False, default=0)
    UCIheight = Column(Integer,default=0)
    UCIwidth = Column(Integer,default=0)

class UClike(Base):
    __tablename__ = 'UClike'
    UCLid = Column(Integer, primary_key=True)
    UClikeid = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE'))  #作品集id
    UClikeUserid = Column(Integer, ForeignKey(User.Uid, onupdate='CASCADE'))
    UCLvalid = Column(Boolean, nullable=False, default=1)
    UCLTime = Column(DateTime(timezone=True), default=func.now())
class UCcomment(Base):
    __tablename__ = 'UCcomment'
    UCCid = Column(Integer, primary_key=True)
    UCcomvalid = Column(Boolean, nullable=False, default=1)
    UCcommentid = Column(Integer, ForeignKey(UserCollection.UCid, onupdate='CASCADE'))
    UCcommentUserid = Column(Integer, ForeignKey(User.Uid, onupdate='CASCADE'))
    UCcontent = Column(VARCHAR(128))
    UCcommentTime = Column(DateTime(timezone=True), default=func.now())





