from django.contrib import admin
from backend import models


# 注册model Admin
admin.site.register(models.Category)
admin.site.register(models.Article)