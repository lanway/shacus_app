#-*- coding:utf-8 -*-
import time
import urllib2
from Database.models import get_db
from Database.tables import User, UserHomepageimg, Image, UserCollection, UserCollectionimg, UClike, UserImage
from FileHandler.Upload import AuthKeyHandler


class UserImgHandler(object):

    # 根据下载凭证生成图片名
    def getpicurl(self,name):
        str = name.split("/")
        str2 = str[4].split("?")
        str[3] = str[3] +'/'+str2[0]
        return str[3]
    # 删除个人照片
    def delete_Homepage_image(self,list,uid):
        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Uid == uid).one()
            for imageitem in list:
                try:
                    imageitemurl = self.getpicurl(imageitem)
                    deleteimage = db.query(UserHomepageimg).filter(UserHomepageimg.UHpicurl == imageitemurl,UserHomepageimg.UHuser==userinfo.Uid).one()
                    deleteimage.UHpicvalid = 0
                    db.commit()
                except Exception, e:
                    print e
                    print '没有找到删除的图片'+imageitem
        except Exception, e:
            print e
            print 'the user doesn\'t exsit'
    # 添加个人照片
    def insert_Homepage_image(self,list,uid):
        try:
            db = get_db()
            userinfo = db.query(User).filter(User.Uid == uid).one()
            for picurl in list:
                try:
                    isexist = db.query(UserHomepageimg).filter(UserHomepageimg.UHpicurl == picurl,UserHomepageimg.UHuser==userinfo.Uid).one()
                    isexist.UHpicvalid = 1
                    db.commit()
                except Exception, e:
                    # 单张图片插入
                    image = Image(
                        IMvalid=True,
                        IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                        IMname=picurl
                    )
                    db.merge(image)
                    db.commit()
                    auth = AuthKeyHandler()
                    try:
                        # 获取图片大小的Json对象
                        sizedata = auth.getsize(picurl)

                        new_img = get_db().query(Image).filter(Image.IMname == picurl).one()
                        imid = new_img.IMid
                        new_hpimg = UserHomepageimg(
                            UHuser=userinfo.Uid,
                            UHimgid=imid,
                            UHpicurl=picurl,
                            UHpicvalid=True,
                            UHheight=sizedata['height'],
                            UHwidth=sizedata['width'],
                        )
                        db.merge(new_hpimg)
                        db.commit()
                    except Exception, e:
                        print e
        except Exception, e:
            print e


    def insert(self,list):
        '''
        向数据库插入图片链接
        :param list: 图片名的列表
        :table: 应该插入的表名
        :return:
        '''
        new_imids=[]
        for img_name in list:  # 第一步，向Image里表里插入
            image = Image(
                IMvalid=True,
                IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                IMname = img_name
            )
            db=get_db()
            db.merge(image)
            db.commit()
            new_img = get_db().query(Image).filter(Image.IMname == img_name).one()
            imid = new_img.IMid
            new_imids.append(imid)
        return new_imids

    def insert_UserCollection_image(self,list,ucid):
        db = get_db()
        for picurl in list:
            try:
                isexist = db.query(UserCollectionimg).filter(UserCollectionimg.UCIurl==picurl,UserCollectionimg.UCIuser == ucid).one()
                isexist.UHpicvalid = 1
                db.commit()
            except Exception, e:#未找到该图片
                print'插入单张新图片'
                image = Image(
                    IMvalid=True,
                    IMT=time.strftime('%Y-%m-%d %H:%M:%S'),
                    IMname=picurl
                )
                db.merge(image)
                db.commit()
                auth = AuthKeyHandler()
                sizedata = auth.getsize(picurl)
                new_img = get_db().query(Image).filter(Image.IMname == picurl).all()
                imid = new_img[0].IMid
                new_ucimg=UserCollectionimg(
                    UCIuser=ucid,
                    UCIimid=imid,
                    UCIurl=picurl,
                    UCIvalid=1,
                    UCIheight = sizedata['height'],
                    UCIwidth = sizedata['width'],
                )
                db.merge(new_ucimg)
                db.commit()

    def delete_UserCollection_image(self, list, ucid):
        # list:要删除的图片
        try:
            db = get_db()
            for imageitem in list:
                try:
                    imageitemurl = self.getpicurl(imageitem)
                    deleteimage = db.query(UserCollectionimg).filter(UserCollectionimg.UCIurl == imageitemurl,
                                                                     UserCollectionimg.UCIuser == ucid).one()
                    deleteimage.UCIvalid = 0
                    db.commit()
                except Exception, e:
                    print e
                    print '没有找到删除的图片'+imageitem
            db.commit()

        except Exception, e:
            print e
            print 'the usercollection doesn\'t exsit'


    # 得到个人照片大图
    def UHpicget(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid, UserHomepageimg.UHpicvalid == 1).all()  # 返回所有图片项
        if imgs:
            print '有个人照片图片'
            for img in imgs:
                img_url = img.UHpicurl
                img_tokens.append(authkeyhandler.download_originpic_url(img_url)) # 裁剪？1200宽度

        else:
            img_tokens = []
        return img_tokens

    # 得到个人照片缩略图
    def UHpicgetassign(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid, UserHomepageimg.UHpicvalid == 1).all()  # 返回所有图片项

        if imgs:
            print '有图片'
            for img in imgs:
                img_url = img.UHpicurl
                img_info = dict(
                    imageUrl=authkeyhandler.download_abb_url(img_url),
                    width=img.UHwidth/3,
                    height=img.UHheight/3,
                )
                img_tokens.append(img_info)
        else:
            img_tokens = []
        return img_tokens

    # b->c作品集详细信息(包括缩略图url和大图url)
    def UCmodel(self,UCsample,uid):  # UCsample是一个UserCollection对象
        authkeyhandler = AuthKeyHandler()
        img = []
        imgsimple = []
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid ,UserCollectionimg.UCIvalid == 1).all()
        for item in ucimg:
            ucimgurl = item.UCIurl
            img.append(authkeyhandler.download_originpic_url(ucimgurl))   # 大图url
            img_info = dict(
                imageUrl=authkeyhandler.download_abb_url(ucimgurl),
                width=item.UCIwidth/6,
                height=item.UCIheight/6,
            )
            imgsimple.append(img_info)
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCuser=uid,
            UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d'),
            UCtitle=UCsample.UCtitle,
            UCcontent=UCsample.UCcontent,
            UCimg=img,                  # 大图url
            UCsimpleimg=imgsimple,      # 缩略图url
        )
        return ret_uc

    # a->b:作品集列表:某个列表封面的获取
    def UC_simple_model(self,UCsample,uid):
        authkeyhandler = AuthKeyHandler()
        # ucsample是一个UserCollection实例
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid,
                                                         UserCollectionimg.UCIvalid == 1).all()
        if ucimg:
            coverurl = authkeyhandler.download_url(ucimg[0].UCIurl)   # 选取第一张作为封面(缩略图)
            img_info = dict(
                imageUrl=coverurl,
                width=ucimg[0].UCIwidth/2,
                height=ucimg[0].UCIheight/2,
            )
        else:
            img_info = dict(
                imageUrl='',
            )
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d'),
            UCtitle = UCsample.UCtitle,
            UCimg=img_info,
        )
        return ret_uc

    # a:个人主页作品集封面
    def UC_homepage_model(self, UCsample, uid):
        print ''
        authkeyhandler = AuthKeyHandler()
        # ucsample是一个UserCollection实例
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid,
                                                         UserCollectionimg.UCIvalid == 1).all()
        if ucimg:
            coverurl = authkeyhandler.download_assign_url(ucimg[0].UCIurl,200,200)  # 选取第一张作为封面(缩略图)
            img_info = coverurl,
        else:
            img_info = dict(
                imageUrl='',
            )
        ret_uc = dict(
            UCid=UCsample.UCid,
            UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d'),
            UCtitle=UCsample.UCtitle,
            UCimg=img_info,
        )
        return ret_uc

    # 个人主页照片集缩略图(缩略图是正方形)
    def UHgetsquarepic(self,uid):
        img_tokens = []
        authkeyhandler = AuthKeyHandler()
        imgs = get_db().query(UserHomepageimg).filter(UserHomepageimg.UHuser == uid , UserHomepageimg.UHpicvalid == 1).all()  # 返回所有图片项
        if imgs:
            print '有图片'
            for img in imgs:
                img_url = img.UHpicurl
                img_tokens.append(authkeyhandler.download_assign_url(img_url,200,200))
        else:
            img_tokens = []
        return img_tokens

    # 登录页作品集模型
    '''
    单个作品集列表的信息包括昵称 头像 性别 年龄 发布时间 图片总数 前三张图片的略缩形式 点赞人列表（包括头像略缩图和id）
    '''
    def UC_login_model(self,UCsample,uid):  # UCsample是一个UserCollection对象
        authkeyhandler = AuthKeyHandler()
        imgsimple = []
        # 获取发布人的model
        try:
            UserPublishModel = get_db().query(User).filter(User.Uid == uid).one()
        except Exception, e:
            UserPublishModel = ''
            print e
        ucimg = get_db().query(UserCollectionimg).filter(UserCollectionimg.UCIuser == UCsample.UCid,
                                                         UserCollectionimg.UCIvalid == 1).limit(3).all()
        ucimgnum = get_db().query(UserCollection).filter(UserCollectionimg.UCIuser == UCsample.UCid,
                                                         UserCollectionimg.UCIvalid == 1).all()
        try:
            userimg = get_db().query(UserImage).filter(UserImage.UIuid == uid).one()
            userheadimg = authkeyhandler.download_url(userimg.UIurl)
            userpublish = dict(
                UserHeadimg=userheadimg,
                UserGender=UserPublishModel.Usex,
                UserId=uid,
                UserAge=UserPublishModel.Uage,
            )
        except Exception, e:
            userpublish = dict(
                UserHeadimg='查找头像失败',
                UserGender='查找头像失败',
                UserId=uid,
                UserAge='',
            )
            print e
        # 获取图片数
        num = 0
        for item in ucimgnum:
            num += 1

        # 获取三张缩略图
        for item in ucimg:
            ucimgurl = item.UCIurl
            # img.append(authkeyhandler.download_originpic_url(ucimgurl))   # 大图url
            img_info = dict(
                imageUrl=authkeyhandler.download_abb_url(ucimgurl),
                width=item.UCIwidth/6,
                height=item.UCIheight/6,
            )
            imgsimple.append(img_info)

        # 获取点赞人列表 包括:id 和 头像
        UserList = []
        uclikepeople = get_db().query(UClike).filter(UClike.UClikeid == UCsample.UCid).all()
        for item in uclikepeople:
            newid = item.UClikeUserid
            userimg = get_db().query(UserImage).filter(UserImage.UIuid == newid).one()
            UClikeModel = dict(
                userid=newid,
                userheadimg=authkeyhandler.download_url(userimg.UIurl)
            )
            UserList.append(UClikeModel)


        try:
            usermodel = get_db().query(User).filter(User.Uid==uid).one()
            # 转换boolean到int
            gender = 0
            if usermodel.Usex == True:
                gender = 1
            elif usermodel.Usex == False:
                gender = 0
            ret_uc = dict(
                UCid=UCsample.UCid,
                UCuser=uid,
                UCusername=usermodel.Ualais,
                UCusergender=gender,
                UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d'),
                UCtitle=UCsample.UCtitle,
                UCcontent=UCsample.UCcontent,
                UCsimpleimg=imgsimple,  # 缩略图url
                UCpicnum=num,  # 作品集图片数
                UserPublish=userpublish,
                UserlikeList=UserList,
            )
            return ret_uc
        except Exception, e:
            usermodel = 'cannot find usermodel'
            print e
            ret_uc = dict(
                UCid=UCsample.UCid,
                UCuser=uid,
                UCmodel = usermodel,
                UCcreateT=UCsample.UCcreateT.strftime('%Y-%m-%d'),
                UCtitle=UCsample.UCtitle,
                UCcontent=UCsample.UCcontent,
                UCsimpleimg=imgsimple,      # 缩略图url
                UCpicnum=num,             # 作品集图片数
                UserHeadimg=userpublish,  # 发布作者的头像
            )
            return ret_uc

