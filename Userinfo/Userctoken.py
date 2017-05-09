# coding=utf-8
'''
@author :兰威
@type ： 用于获得用户聊天时的token
'''
from Database.models import get_db
from Database.tables import User
from rongcloud import RongCloud


def get_token(uid,nickname):
    rcloud = RongCloud("pvxdm17jxpuvr", "rYwvnaVeAAYYW8")
    c = rcloud.User.getToken(userId=uid, name=nickname,portraitUri='').result
    return c['token']


def update_token():   # 更新token
    db = get_db()
    users = db.query(User).all()
    for user in users:
        token = get_token(user.Uid,user.Ualais)
        user.Uchattoken = token
        db.commit()

# update_token()


