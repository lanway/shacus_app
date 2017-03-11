# -*- coding: utf-8 -*-
'''
@author:王佳镭
'''
from Database.models import get_db
from Database.tables import Favorite
from FileHandler.Upload import AuthKeyHandler
def TRresponse(item,url,retdata,isfav):
    authkey= AuthKeyHandler()
    m_trresponse = dict (
        Tid=item.Tid,
        Tsponsorid=item.Tsponsorid,
        TsponsT=item.TsponsT.strftime('%Y-%m-%dT%H:%M:%S'),
        TcommentN=item.TcommentN,
        TlikeN=item.TlikeN,
        Tcontent=item.Tcontent,
        Ttitle=item.Ttitle,
        Tsponsorimg = authkey.download_url(item.Tsponsorimg),
        TIimgurl=authkey.download_url(url),
        TIisfavorite=isfav,
    )
    retdata.append(m_trresponse)