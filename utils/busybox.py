#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 下午3:15
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : busybox.py
# @Software: PyCharm
# @describe: 一些使用的工具集

import hashlib
# from libgravatar import Gravatar
#
#
# def get_avatar_form_gravatar(email=None, size=40):
#     """
#     根据邮箱获取用户的gravatar头像
#     :param email: 需要用户提供用户的邮箱
#     :param size: 提供图片的大小，默认是40*40的大小。大小可以使1~2048
#     :return:
#     """
#     g = Gravatar(email)
#     url = g.get_image(size=size)
#     return url


def get_rand_str(encrypt, salt='dcgamer.top', coding='utf8'):
    """
    给自己使用的一个加密生成随机字符串的方法
    :param encrypt: 需要加密的关键字
    :param salt: 加盐
    :param coding: 编码方式，unicode对象在hash之前需要进行转码
    :return:
    """
    md5 = hashlib.md5()
    md5.update(encrypt.encode(coding))
    if salt:
        if isinstance(salt, str):
            md5.update(salt.encode(coding))
    return md5.hexdigest()




