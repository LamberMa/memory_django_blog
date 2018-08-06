#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 下午2:52
# @Author  : lamber
# @Site    : dcgamer.top
# @File    : forms.py
# @Software: PyCharm
from django.forms import Form, widgets, fields
from backend import models


class ArticleForm(Form):
    """后台与文章提交相关的Form组件类"""
    title = fields.CharField(
        max_length=128,
        label='撰写文章标题',
        required=True,
        error_messages={
            'required': '标题不能为空',
            'max_length': '最大请不要超过128个字符',
        },
        widget=widgets.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入标题'}
        ),
    )
    summary = fields.CharField(
        label="文章摘要",
        widget=widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 3}
        )
    )
    content = fields.CharField(
        widget=widgets.Textarea({})
    )

    category = fields.MultipleChoiceField(
        label='文章分类',
        choices=models.Category.objects.values_list('nid', 'title'),
        widget=widgets.SelectMultiple({
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        """
        通过父类的构造方法添加self.fields动态的添加新增加的分类项
        :param args:
        :param kwargs:
        """
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = models.Category.objects.values_list('nid', 'title')
from django.db.backends.mysql import base
from django.db.backends import utils
from django.core.management import execute_from_command_line