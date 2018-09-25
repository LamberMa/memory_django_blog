from django.contrib import admin
from backend import models


# 注册model Admin
admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Tag)
admin.site.register(models.Article2Tag)
