# Generated by Django 2.0.3 on 2018-03-19 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('summary', models.CharField(default='', max_length=255, verbose_name='文章简介')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='班级名')),
                ('course', models.CharField(max_length=32, verbose_name='课程')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=23, verbose_name='姓名')),
                ('classes', models.ManyToManyField(to='main.Class', verbose_name='所属班级')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('avatar', models.ImageField(upload_to='static/imgs', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Category', verbose_name='文章类型'),
        ),
    ]
