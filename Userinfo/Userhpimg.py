# coding=utf-8
# 个人主页图片：包括个人照片和作品集
import json
import threading
from BaseHandlerh import BaseHandler
from Database.models import get_db
from Database.tables import User, UserHomepageimg, UserCollection
from FileHandler.Upload import AuthKeyHandler
from Userinfo.UserImgHandler import UserImgHandler


class Userhpimg(BaseHandler):

    def post(self):
        type = self.get_argument('type')

        # 添加个人图片:第一步返回token
        if type=='10808':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  #验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    retjson_body = {'auth_key': '', 'uid': ''}
                    auth_key_handler = AuthKeyHandler()
                    retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)    # 上传凭证
                    retjson_body['uid']= userid.Uid
                    retjson['contents'] = retjson_body   # 返回图片的token
                    retjson['code']= '10808'
            except Exception, e:
                print e
                retjson['code']='10809'
                retjson['contents']='验证失败'

        # 插入图片第二步(插入数据库)
        elif type == '10810':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  #验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    imhandler= UserImgHandler()
                    imhandler.insert_Homepage_image(ap_imgs_json,u_id)

                    retjson['code']= '10810'
                    retjson['contents'] = '数据库操作成功'
                else:
                    print '验证码错误'
                    retjson['code'] = '10810'
                    retjson['contents'] = '验证未通过'
            except Exception, e:
                print e
                retjson['code']='10810'
                retjson['contents']='查找用户失败'

        # 删除图片
        elif type == '10811':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid == u_id).one()
                key = userid.Uauthkey
                if key == auth_key:  # 验证通过
                    print '验证通过'
                    print imgs
                    ap_imgs_json = json.loads(imgs)
                    print ap_imgs_json
                    imhandler = UserImgHandler()
                    imhandler.delete_Homepage_image(ap_imgs_json, u_id)
                    retjson['code'] = '10811'
                    retjson['contents'] = '数据库操作成功'
                else:
                    print '验证码错误'
                    retjson['code'] = '10811'
                    retjson['contents'] = '验证未通过'
            except Exception, e:
                print e
                retjson['code'] = '10811'
                retjson['contents'] = '查找用户失败'

        # 获取个人主页缩略图(200*200)
        elif type == '10812':
            retjson = {'code': '', 'contents': ""}
            uhuser = self.get_argument('uid')
            authkey = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()
                if userid:  # 验证通过
                    img= UserImgHandler()
                    try:
                        piclist = img.UHgetsquarepic(uhuser)
                        retjson['code']='10812'
                        retjson['contents']= piclist
                    except Exception, e:
                        print e
                        retjson['code'] = '10811'
                        retjson['contents'] = '获取图片信息失败'
                else:
                    print'认证错误'
                    retjson['code']='10813'
                    retjson['contents']= '用户认证错误'
            except Exception, e:
                print e
                retjson['code']='10813'
                retjson['contents']='未找到该用户'

        # 获取个人缩略图片和大图url(个人主页点进去)
        elif type == '10814':
            retjson = {'code': '', 'contents': ""}
            uhuser = self.get_argument('uid')
            authkey = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uauthkey == authkey).one()
                if userid.Uid == uhuser:
                    isself = 1
                else:
                    isself = 0
                img= UserImgHandler()
                piclist = img.UHpicget(uhuser)
                piclist02 = img.UHpicgetassign(uhuser)
                retjson['code'] = '10814'
                retjson['isself'] = isself
                retjson['originurl'] = piclist
                retjson['contents'] = piclist02
            except Exception, e:
                print e
                retjson['code']='10815'
                retjson['contents']='未找到该用户'

        # 发布作品集(第一步返回token)
        elif type == '10804':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            uc_title = self.get_argument('title')
            try:
                userid = self.db.query(User).filter(User.Uid==u_id).one()
                key = userid.Uauthkey
                if key== auth_key:  # 验证通过
                    print '验证通过'
                    ap_imgs_json = json.loads(imgs)
                    retjson_body = {'auth_key': '', 'ucid': ''}
                    auth_key_handler = AuthKeyHandler()
                    retjson_body['auth_key'] = auth_key_handler.generateToken(ap_imgs_json)  # 上传凭证
                    # 插入数据库
                    try:
                        new_usercollection = UserCollection(
                            UCuser=u_id,
                            UCtitle=uc_title,
                            UCcontent='',
                            UCvalid=0,
                            UCiscollection=0,
                        )
                        self.db.merge(new_usercollection)
                        self.db.commit()
                    except Exception,e :
                        print e
                        retjson['contents']='数据库插入失败'
                    try:
                        print '插入成功，进入查询'
                        uc = self.db.query(UserCollection).filter(
                           UserCollection.UCtitle == uc_title, UserCollection.UCuser == u_id).one()
                        ucid = uc.UCid
                        retjson_body['ucid'] = ucid
                        retjson['contents'] = retjson_body
                        retjson['code']='10804'
                    except Exception, e:
                        print '插入失败！！'
                        retjson['contents'] = r'服务器插入失败'
                else:
                    retjson['code']= '10805'
                    retjson['contents']= '用户认证失败'
            except Exception, e:
                    print e
                    retjson['code'] = '10805'
                    retjson['contents'] = "该用户名不存在"

        # 发布作品集(第二步插入数据库)
        elif type == '10806':
            retjson = {'code': '', 'contents': ""}
            print "进入10806"
            uc_id = self.get_argument('ucid')
            auth_key = self.get_argument('authkey')
            ap_title = self.get_argument('title')
            uc_content = self.get_argument('content')
            uc_imgs = self.get_argument('imgs')
            try:

                self.db.query(UserCollection).filter(UserCollection.UCid == uc_id).\
                                    update({ UserCollection.UCcontent: uc_content,
                                             UserCollection.UCvalid: 1,
                                             UserCollection.UCtitle:ap_title,
                                            }, synchronize_session=False)
                self.db.commit()
                print '更新完成'
                try:
                    imghandler = UserImgHandler()
                    uc_images_json=json.loads(uc_imgs)
                    imghandler.insert_UserCollection_image(uc_images_json,uc_id)
                    self.db.commit()
                    retjson['code'] = '10806'
                    retjson['contents'] = '修改/发布作品集成功'
                except Exception, e:
                    print e
                    retjson['code']='10806'
                    retjson['contents'] = u'插入图片表失败'
            except Exception, e:
                print e

            #删除【一个】作品集的图片

        # 作品集删除图片
        elif type == '10820':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            uc_id = self.get_argument('ucid')
            try:
                userid = self.db.query(User).filter(User.Uid == u_id).one()
                key = userid.Uauthkey
                if key == auth_key:  # 验证通过
                    print '作品集删除' \
                          '图片验证通过'
                    ap_imgs_json = json.loads(imgs)
                    imhandler = UserImgHandler()
                    imhandler.delete_UserCollection_image(ap_imgs_json,uc_id)
                    get_db().commit()
                    retjson['code'] = '10820'
                    retjson['contents'] = '数据库操作成功'
                else:
                    retjson['code'] = '10821'
                    retjson['contents'] = '认证失败'
            except Exception, e:
                print e
                retjson['code'] = '10821'
                retjson['contents'] = '未找到此用户'

        #删除作品集
        elif type == '10826':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            auth_key = self.get_argument('authkey')
            uc_id = self.get_argument('ucid')
            try:
                userid = self.db.query(User).filter(User.Uid == u_id).one()
                key = userid.Uauthkey
                if key == auth_key:  # 验证通过
                    print '删除作品集验证通过'
                    ucidlist = json.loads(uc_id)
                    for item in ucidlist:
                        user_collection = self.db.query(UserCollection).filter(UserCollection.UCid == item).one()
                        user_collection.UCvalid = 0
                        self.db.commit()
                    retjson['code'] = '10826'
                    retjson['contents'] = '删除作品集成功'
                else:
                    retjson['code'] = '10827'
                    retjson['contents'] = '认证失败'
            except Exception, e:
                print e
                retjson['code'] = '10827'
                retjson['contents'] = '未找到此用户'

        #作品集添加图片step1
        elif type == '10822':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            try:
                userid = self.db.query(User).filter(User.Uid == u_id).one()
                key = userid.Uauthkey
                if key == auth_key:  # 验证通过
                    print '作品集添加图片(first step)'
                    ap_imgs_json = json.loads(imgs)
                    auth_key_handler = AuthKeyHandler()
                    retjson['contents'] = auth_key_handler.generateToken(ap_imgs_json)  # 返回图片的token
                    retjson['code'] = '10822'
            except Exception, e:
                print e
                retjson['code'] = '10823'
                retjson['contents'] = '验证失败'
        # 添加作品集图片
        elif type == '10824':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            imgs = self.get_argument('imgs')
            auth_key = self.get_argument('authkey')
            uc_id = self.get_argument('ucid')
            uc_content =self.get_argument('content')
            uc_title = self.get_argument('title')
            try:
                userid = self.db.query(User).filter(User.Uid == u_id).one()
                key = userid.Uauthkey
                if key == auth_key:  # 验证通过
                    print '验证通过'
                    self.db.query(UserCollection).filter(UserCollection.UCid == uc_id). \
                        update({UserCollection.UCcontent: uc_content,
                                UserCollection.UCvalid: 1,
                                UserCollection.UCtitle: uc_title,
                                }, synchronize_session=False)
                    self.db.commit()
                    print '更新完成'
                    ap_imgs_json = json.loads(imgs)
                    imhandler = UserImgHandler()
                    imhandler.insert_UserCollection_image(ap_imgs_json,uc_id)
                    self.db.commit()
                    retjson['code'] = '10824'
                    retjson['contents'] = '数据库操作成功'
                else:
                    retjson['code'] = '10824'
                    retjson['contents'] = '认证失败'
            except Exception, e:
                print e
                retjson['code'] = '10824'
                retjson['contents'] = '未找到此用户'

        # 获取作品集列表(缩略图+时间标题)
        elif type == '10818':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            auth_key = self.get_argument("authkey")
            try:
                userid = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                if userid.Uid == u_id:
                    isself = 1
                else:
                    isself = 0
                retjson['isself'] = isself
                imghandler = UserImgHandler()
                retdata = []
                pic = self.db.query(UserCollection).filter(UserCollection.UCuser == u_id,UserCollection.UCvalid == 1).all()
                print '进入作品集列表获取'
                try:
                    for item in pic:
                        retdata.append(imghandler.UC_simple_model(item,u_id))
                    retjson['code'] = '10818'
                    retjson['contents'] = retdata
                except Exception ,e:
                    print e
            except Exception, e:
                print e
                retjson['contents'] = '用户认证失败'

        # 获取【单个】作品集信息（包括缩略图url和大图url）
        elif type == '10816':
            print ''
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            auth_key = self.get_argument("authkey")
            uc_id = self.get_argument('ucid')
            imghandler=UserImgHandler()
            try:
                userid = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                if userid.Uid == u_id:
                    isself = 1
                else:
                    isself = 0
                try:
                    pic = self.db.query(UserCollection).filter(UserCollection.UCid == uc_id).one()
                    retjson['code']='10816'
                    retjson['isself'] = isself
                    retjson['contents']= imghandler.UCmodel(pic,u_id)
                except Exception, e:
                    print e
                    retjson['code']='10817'
                    retjson['contents'] = '没有这个作品'
            except Exception, e:
                print e
                retjson['contents'] = '用户认证失败'

        # 获取个人主页作品集封面(200*200)
        elif type == '10828':
            retjson = {'code': '', 'contents': ""}
            u_id = self.get_argument('uid')
            auth_key = self.get_argument("authkey")
            try:
                userid = self.db.query(User).filter(User.Uauthkey == auth_key).one()
                imghandler = UserImgHandler()
                retdata = []
                pic = self.db.query(UserCollection).filter(UserCollection.UCuser == u_id,UserCollection.UCvalid == 1).all()
                print '进入作品集列表获取'
                try:
                    for item in pic:
                        retdata.append(imghandler.UC_homepage_model(item,u_id))
                    retjson['code'] = '10828'
                    retjson['contents'] = retdata
                except Exception, e:
                    print e
            except Exception, e:
                print e
                retjson['contents'] = '用户认证失败'
        self.write(json.dumps(retjson, ensure_ascii=False, indent=2))

