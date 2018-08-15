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
        max_length='255',
        error_messages={
            'required': '摘要请不要留空',
            'max_length': '最大请不要超过255个字符',
        },
        widget=widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 3}
        )
    )
    content = fields.CharField(
        error_messages={'required': '正文请不要留空', },
        widget=widgets.Textarea({})
    )

    category = fields.ChoiceField(
        label='文章分类',
        error_messages={'required': '必须选择一个分类', },
        choices=models.Category.objects.values_list('nid', 'title'),
        widget=widgets.Select(
            attrs={'class': 'form-control'}
        )
    )

    tag = fields.CharField(
        label="文章标签",
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
        })
    )

    imgfile = fields.CharField(
        label="文章题图",
        # 目前传题图不是必要的
        required=False,
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
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
