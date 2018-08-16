#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/16 下午3:35
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : qiniutools.py
# @Software: PyCharm
# 官方SDK：https://developer.qiniu.com/kodo/sdk/1242/python
"""
在设置回调函数的时候，其实有个问题就是它发的是一个post请求，因此会很蛋疼的被django的csrf给干掉，
所以我这里只能先使用csrf的装饰器绕过csrf的验证。
关于七牛云上传的响应
https://blog.csdn.net/guoer9973/article/details/45916709
"""
from qiniu import Auth, put_file, etag

# import qiniu.config


class QN:

    def __init__(self, access_key, secret_key, bucket_name, filename, url,
                 callback=True, expire=3600, ):
        """
        初始化七牛云插件
        :param access_key: 用户的access_key
        :param secret_key: 用户的secret_key
        :param bucket_name: 用户的对象存储空间
        :param callback: 是否需要七牛云的的回调内容，默认需要回调需要业务端设置回调函数，返回一个json状态
        :param expire: 超时时间，默认是3600s
        :param filename: 上传文件名，这个上传文件名指的是上传到七牛云那里是什么名字，实际我们取的时候也是拿这个
        :param url: 回调url
        :parameter policy: 回调时需要的策略
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.auth = self._auth()
        self.bucket_name = bucket_name
        self.callback = callback
        self.expire = expire
        self.filename = filename
        self.url = url
        self.policy = {
            'callbackUrl': url,
            'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
        }

    def _auth(self):
        """构建鉴权对象，需要填入用户的access_key和secret_key"""
        return Auth(self.access_key, self.secret_key)

    def _get_upload_token(self):
        """
        生成上传 Token，可以指定过期时间等，policy是当需要回调的时候才需要的参数，如果不需要回调可以传递一个空字典
        :return: 上传用token
        """
        if not self.callback:
            self.policy = {}
        return self.auth.upload_token(self.bucket_name, self.filename, self.expire, self.policy)

    def upload(self, localurl):
        """
        上传函数
        :param localurl: 要上传的本地文件的路径
        :return: ret：回调业务服务返回的字典，info：response_info
        """
        ret, info = put_file(self._get_upload_token(), self.filename, localurl)
        return ret, info


up = QN('oW59DcqC9H89DxEKAJyEbvTx6R7EuA7K2-2rlcF-',
        'zJk139xsjfqEtR-rdohtp5rVOa2wNWJ6IDQzqE6r',
        'blog-storage',
        'uploadfile.png',
        'http://memory.dcgamer.top/qiniutest.html')

ret1, info1 = up.upload('../123.png')

print('info', info1)
print('ret:', ret1)
# assert ret1['key'] == key
# assert ret1['hash'] == etag(localfile)
