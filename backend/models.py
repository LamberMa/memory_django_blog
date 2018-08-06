from django.db import models

# Create your models here.
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

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """文章表，用户保存用户文章相关信息"""
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255, default='')
    read_count = models.IntegerField(default=0, verbose_name='阅读数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    up_count = models.IntegerField(default=0, verbose_name='点赞数')
    down_count = models.IntegerField(default=0, verbose_name='踩数量')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, )
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', null=True,
                                 on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag",
        through_fields=('article', 'tag')
    )

    def __str__(self):
        return self.title

    class Meta:
        """
        添加这个meta元类，定义verbose_name就可以在admin中见到中文的字段拉啦
        db_table可以指定在数据库生成的名字到底是什么而不是根据django自己的命名
        verbose_name的复数会在我们的中文名后面加一个s，我们让它就等于我们设置的verbose_name就好了
        因为它是是用歪国人写的嘛。
        """
        # db_table = 'xxx'
        verbose_name = '文章表'
        verbose_name_plural = verbose_name


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容', )
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]


class Category(models.Model):
    """
        博主个人文章分类表
        """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "分类表"
        verbose_name_plural = verbose_name


class UserType(models.Model):
    caption = models.CharField(max_length=32)

    def __str__(self):
        return self.caption
