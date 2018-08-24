#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/2 下午5:39
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : urls.py
# @Software: PyCharm


from django.urls import path, include
from backend import views

urlpatterns = [
    # 直接访问后台的时候，管理后台的界面
    path('', views.index),
    path('article/', views.edit_article),
    path('article2/', views.article2),
    path('uploadimg/', views.uploadimg),
    path('user/', views.user),
    path('test/', views.aaa)
]