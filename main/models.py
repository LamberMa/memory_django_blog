from django.db import models


# Create your models here.
class User(models.Model):
    """用户表，用户保存用户相关信息"""

    uid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=128)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', upload_to='static/imgs')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.nickname


class Article(models.Model):
    """文章表，用于保存文章相关信息"""
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    pass


class Category(models.Model):
    """
        博主个人文章分类表
        """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    def __str__(self):
        return self.title




