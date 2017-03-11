#-*- coding:-utf-8 -*-
'''
@author:王佳镭
'''
from tokenize import String

from Database.models import get_db
from Database.tables import ActivityLike, Activity
from FileHandler.Upload import AuthKeyHandler

def response(item,retdata,url,Usermodel,issponsor,userid):#查看活动更多详情
    liked = 0
    try:
        likedentry = get_db().query(ActivityLike).filter(ActivityLike.ACLuid == userid,
                                                        ActivityLike.ACLacid == item.ACid,
                                                        ActivityLike.ACLvalid == 1).one()  # 寻找是否点过赞
        if likedentry:
            liked = 1
            print "点过赞", liked
    except Exception, e:
        print e
        liked = 0
    ACregister = []
    m_response=dict(
        ACid=item.ACid,
        ACsponsorid=item.ACsponsorid,
        AClocation=item.AClocation,
        ACtitle=item.ACtitle,
        ACtag=item.ACtag,
        ACstartT=item.ACstartT.strftime('%Y-%m-%d %H:%M:%S'),
        ACendT=item.ACendT.strftime('%Y-%m-%d %H:%M:%S'),
        ACjoinT=item.ACjoinT.strftime('%Y-%m-%d %H:%M:%S'),
        ACcontent=item.ACcontent,
        ACfree=int(item.ACfree),
        ACprice=item.ACprice,
        ACclosed=int(item.ACclosed),
        ACcreateT=item.ACcreateT.strftime('%Y-%m-%d %H:%M:%S'),
        ACcommentnumber=item.ACcommentnumber,
        ACmaxp=item.ACmaxp,
        ACminp=item.ACminp,
        ACscore=item.ACscore,
        AClikenumber=item.AClikenumber,
        ACvalid=int(item.ACvalid),
        ACstatus = item.ACstatus,
        ACimageurl = url,
        ACregister=Usermodel,
        AC_issponsor=issponsor,
        Userliked = liked
    )
    retdata.append(m_response)


def Acresponse(item,item2,aclurl,userurl,retdata,userid):
    auth = AuthKeyHandler()
    liked = 0
    try:
        likedentry = get_db().query(ActivityLike).filter(ActivityLike.ACLuid == userid,
                                                         ActivityLike.ACLacid == item.ACid,
                                                         ActivityLike.ACLvalid == 1).one()  # 寻找是否点过赞
        if likedentry:
            liked = 1
            print "点过赞", liked
    except Exception, e:
        print e
        liked = 0

    m_Acresponse=dict(
        ACid=item.ACid,
        ACtitle=item.ACtitle,
        ACsponsorid=item.ACsponsorid,#username
        AClocation=item.AClocation,#location
        ACcontent=item.ACcontent,#
        ACstartT=item.ACstartT.strftime('%Y-%m-%dT%H:%M:%S'),#settime
        AClikenumber=item.AClikenumber,#praisenum
        ACregistN=item.ACregistN,#joinnum
        AClurl=auth.download_url(aclurl),
        Userimageurl=auth.download_url(userurl),
        Ualais=item2.Ualais,
        Userliked=liked
    )
    retdata.append(m_Acresponse)

# def ACregister(item,item2):
#     m_ACregisterlist= []
#     m_ACregisterdict={'Uid':'','Userurl':''}
#
#     entryid=item
#     Userurl=item2
#
#     m_ACregisterlist.append(m_ACregisterdict)
