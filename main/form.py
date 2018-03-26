from django.db import models
from django.forms import fields, Form


class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': '不能为空',
            'min_length': '太短了！',
            'max_length': '太长了！！！！',
        }
    )
    password = fields.CharField(
        max_length=16,
        required=True,
        min_length=6,
    )
    t2 = fields.IntegerField()


