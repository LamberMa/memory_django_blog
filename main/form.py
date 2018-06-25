from django.db import models
from django.forms import fields, Form


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': '用户名不能为空不能为空',
            'min_length': '请不要输入少于6个字符',
            'max_length': '请不要输入超过18个字符',
        }
    )
    password = fields.CharField(
        max_length=16,
        required=True,
        min_length=6,
        error_messages={
            'required': "密码不能为空"
        }
    )
    t2 = fields.IntegerField()


