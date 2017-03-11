# -*- coding: utf-8 -*-
'''
@author: 黄鑫晨
'''
#!/usr/bin/env python
import tornado.httpserver
import  tornado.ioloop
import  tornado.options
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options

from Activity.ACHandler import ActivityCreate, ActivityRegister
from Activity.ACaskHandler import AskActivity
from Activity.ACentryHandler import AskEntry
from Appointment.APAskHandler import APaskHandler
from Appointment.APCreateHandler import APcreateHandler
from Appointment.APRegistHandler import APregistHandler
from Appointment.APchatCreateHandler import APchatCreateHandler
from Appointment.APpraseHandler import APprase
from Appointment.Ranklist import Ranklist
from Course.Chomepage import Chomepage
from Course.CourseAsk import CourseAsk
from Course.CourseLike import Courselike
from Course.Coursefav import Coursefav
from Database.models import engine
from ImageCallback import ImageCallback
from Pressuretest import login
from Pressuretest.Simplerequest import Simplerequest
from RegisterHandler import RegisterHandler
from Settings import PaswChange
from TRends.TRendspost import TRendspost
from TRends.TrendHandler import TrendHandler
from Userinfo.UserCollectionHandler import UserCollectionHandler
from Userinfo.UserFavoriteHandler import UserFavorite
from Userinfo.UserImgHandler import UserImgHandler
from Userinfo.UserIndent import UserIndent
from Userinfo.UserInfo import UserInfo
from Userinfo.UserLike import FindUlike
from Userinfo.Userhomepager import Userhomepager
from Userinfo.Userhpimg import Userhpimg
from loginHandler import LoginHandler
define("port", default=800, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r"/appointment/create", APcreateHandler),
             (r"/pressuretest",Simplerequest),
             (r"/pressuretest2", login.login),
             (r"/appointment/ask", APaskHandler),
             (r"/appointment/prase", APprase),
             (r"/appointment/regist", APregistHandler),
             (r"/login", LoginHandler),
             (r"/regist", RegisterHandler),
             (r"/user/homepager",Userhomepager),
             (r"/user/mylike", FindUlike),
             (r"/user/favorite", UserFavorite),
             (r"/user/info",UserInfo),
             (r"/user/indent",UserIndent),
             (r"/Activity/ask", AskActivity),
             (r"/Activity/entry", AskEntry),
             (r"/activity/create", ActivityCreate),
             (r"/activity/register",ActivityRegister),
             (r"/ImageCallback",ImageCallback),
             (r"/PaswChange",PaswChange),
             (r"/trend/Trendspost",TRendspost),
             (r"/trend/Trendhanler",TrendHandler),
             (r"/course/homepage",Chomepage),
             (r"/course/ask",CourseAsk),
             (r"/course/like",Courselike),
             (r"/course/fav",Coursefav),
             (r"/ranklist", Ranklist),
             (r"/appointment/chat",APchatCreateHandler),
             (r"/Userinfo/imghandler",Userhpimg),
             (r"/Userinfo/CollectionHandler",UserCollectionHandler),
        ]
        tornado.web.Application.__init__(self, handlers)
        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False, autoflush=True,
                                              expire_on_commit=False))

# session负责执行内存中的对象和数据库表之间的同步工作 Session类有很多参数,使用sessionmaker是为了简化这个过程
if __name__ == "__main__":
    print "HI,I am in main "
    tornado.options.parse_command_line()
    Application().listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()

