#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/26 下午3:15
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : busybox.py
# @Software: PyCharm

from libgravatar import Gravatar


def get_avatar_form_gravatar(email=None, size=40):
    """
    根据邮箱获取用户的gravatar头像
    :param email: 需要用户提供用户的邮箱
    :param size: 提供图片的大小，默认是40*40的大小。大小可以使1~2048
    :return:
    """
    g = Gravatar(email)
    url = g.get_image(size=size)
    return url

