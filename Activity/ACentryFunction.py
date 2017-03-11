#-*- coding:utf-8 -*-
'''
@author：王佳镭
'''
def response(item,retdata):
    m_response=dict(
    ACEid=item.ACEid,
    ACEacid=item.ACEacid,#活动id
    ACEregisterid=item.ACEregisterid,#报名人id
    ACEregisttvilid=item.ACEregisttvilid,
    ACEscore=item.ACEscore,
    ACEcomment=item.ACEcomment,
    ACEregisterT=item.ACEregisterT.strftime('%Y-%m-%d %H:%M:%S'),
    )
    retdata.append(m_response)

