from django.contrib import admin
from main import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.User)
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Class)
admin.site.register(models.UserType)
admin.site.register(models.UserInfo)