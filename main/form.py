from django.db import models
from django.forms import fields, Form, widgets


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空不能为空',
            'min_length': '请不要输入少于6个字符',
            'max_length': '请不要输入超过18个字符',
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入您的用户名'
        }),
    )
    password = fields.CharField(
        max_length=16,
        required=True,
        min_length=6,
        error_messages={
            'required': "密码不能为空"
        },
        widget=widgets.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入您的密码'
        })
    )
    t2 = fields.IntegerField()


# 用户注册相关Form组件定义
class RegisterForm(Form):

    # 用户名form组件
    username = fields.CharField(
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_lenght': '最大长度请不要超过32',
            'min_length': '请输入至少6个字符',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入您的用户名',
            }
        )
    )
    # 用户昵称form组件
    nickname = fields.CharField(
        max_length=32,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空',
            'max_lenght': '最大长度请不要超过32个字符',
            'min_length': '请输入至少6个字符',
        }
    )
    # 用户性别
    gender = fields.CharField(
        choices=((1, '男'), (2, '女'),),
        initial=2,
        widget=widgets.RadioSelect
    )
    # 用户密码form组件
    password = fields.CharField(
        max_length=32,
        min_length=10,
        required=True,
        error_messages={
            'required': '密码为必填字段，请不要留空',
            'max_length': '最大长度请不要超过32个字符',
            'min_length': '密码长度不要小于10个字符',
        }
    )
    # 确认密码form组件
    re_password = fields.CharField(
        max_length=32,
        min_length=10,
        required=True,
        error_messages={
            'required': '密码为必填字段，请不要留空',
            'max_length': '最大长度请不要超过32个字符',
            'min_length': '密码长度不要小于10个字符',
        }
    )