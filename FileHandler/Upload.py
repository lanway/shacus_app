# -*- coding: utf-8 -*-
# flake8: noqa
'''
 作用：处理七牛云上传凭证获取
 创建者：兰威
 创建时间：2016-08-30 18:05
'''
import json
import urllib2

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

# todo 封装auth_token
class AuthKeyHandler:
    def __init__(self):
        self.access_key = 'yzAza_Cm87nXkh9IyFfpg7LL7qKJ097VK5IOpLj0'
        self.secret_key = 'GFWHU9hYkU4hepDwpWfHaNDt3gJCDsAk3Kz6DGdk'
        self.Auth_key = Auth(self.access_key, self.secret_key)
        self.auth_tokens = []
    # 构建鉴权对象
    def generateToken(self,names):
       bucket_name = 'shacus' # 要上传的空间
       tokens = []
       for title in names:
           print 'title:',title
           token = self.Auth_key.upload_token(bucket_name, title, 345600)
           self.auth_tokens.append(token)
       return self.auth_tokens
    def get_auth_key(self):
        return self.Auth_key
    def get_token(self):
        return self.auth_tokens
    def download_url(self,name):
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        base_url  = 'http://%s/%s' % (bucket_domain, name )
        private_url =auth.private_download_url(base_url, expires=3600)
        return private_url

    def download_assign_url(self,name,width,heigh):
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        base_url = 'http://{bucket}/{name}?imageView2/1/w/{width}/h/{heigh}'.format(bucket=bucket_domain,name=name,width=width,heigh=heigh)
        private_url = auth.private_download_url(base_url, expires=3600)
        return private_url
    def download_abb_url(self,name):
        '''
        下载略缩图链接
        Args:
            name: 图片名字

        Returns:图片下载地址

        '''
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        base_url = 'http://%s/%s?imageView2/2/w/200' % (bucket_domain, name)
        private_url =auth.private_download_url(base_url, expires=3600)
        #private_url = private_url+"&imageView2/2/w/200"
        return private_url

    def download_originpic_url(self,name):
        '''
        下载宽度为1200按比例缩放图片
        Args:
            name: 图片名字

        Returns:图片下载地址

        '''
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        base_url = 'http://%s/%s?imageView2/2/w/1200' % (bucket_domain, name)
        private_url =auth.private_download_url(base_url, expires=3600)
        return private_url

    def getsize(self,name):
        auth = self.get_auth_key()
        bucket_domain = 'oci8c6557.bkt.clouddn.com'
        originurl = 'http://%s/%s?imageInfo' % (bucket_domain, name )
        private_url = auth.private_download_url(originurl, expires=3600)
        print 'urllib2----------'
        req = urllib2.Request(private_url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        data = json.loads(res)
        return data




