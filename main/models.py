from django.db import models


# Create your models here.
class User(models.Model):
    """用户表，用户保存用户相关信息"""

    uid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=128)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    # avatar = models.ImageField(verbose_name='头像', upload_to='static/imgs')
    avatar = models.ImageField(verbose_name='头像', default='/static/imgs/head/default/default1.jpg')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.nickname


class Article(models.Model):
    """文章表，用于保存文章相关信息"""
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255, default='')
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, )
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    pass


class Class(models.Model):
    name = models.CharField(max_length=32, verbose_name="班级名")
    course = models.CharField(verbose_name="课程", max_length=32, default='', blank=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=23, verbose_name="姓名")
    classes = models.ManyToManyField(verbose_name="所属班级", to="Class")

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name='学生姓名')
    classes = models.OneToOneField(verbose_name="所属班级", to="Class", on_delete=models.CASCADE)
    create_data = models.DateTimeField(verbose_name="学生创建时间", auto_now=True)


class Category(models.Model):
    """
        博主个人文章分类表
        """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=20)


class Publisher(models.Model):
    name = models.CharField(max_length=20)


class Book(models.Model):
    name = models.CharField(max_length=20)
    pub = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)


class TestModel(models.Model):
    test_date1 = models.DateTimeField(null=True, unique=True)
    test_date2 = models.DateTimeField(null=True, unique_for_date=True)
    test_date3 = models.DateTimeField(null=True, unique_for_month=True)
    test_date4 = models.DateTimeField(null=True, unique_for_year=True)


class UserType(models.Model):
    caption = models.CharField(max_length=32)

    def __str__(self):
        return self.caption


class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    age = models.IntegerField()
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE)

    def __str__(self):
        return self.username



