import os
import json

from django.shortcuts import render, HttpResponse, redirect

from backend.forms import ArticleForm
from backend import models


# Create your views here.
def index(request):
    return render(request, 'backend/layout.html')


def edit_article(request):
    return render(request, 'backend/article.html')


def article2(request):
    if request.method == "POST":
        obj = ArticleForm(request.POST)
        if obj.is_valid():
            article_detail = obj.cleaned_data.pop('content')
            models.Article.objects.create()
        else:
            print(obj.errors)
        return HttpResponse('xxxx')
    obj = ArticleForm()
    return render(request, 'backend/article2.html', {'article': obj})


def user(request):
    if request.method == "POST":
        pass
    user_list = models.User.objects.values('uid', 'username', 'nickname', 'email', 'avatar', 'create_time')
    return render(request, 'backend/user.html', {'user_list': user_list})


def uploadimg(request):
    if request.method == "POST":
        file_type = request.GET.get('dir')
        file = request.FILES.get('imgFile')
        file_path = os.path.join('static/imgs/upload', file_type, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        # 给人家程序返回的必须是这个内容
        dic = {
            # error取值0或者是1，url为上传成功的filepath，message表示
            'error': 0,
            'url': "/" + file_path,
            'message': '错了'
        }
        return HttpResponse(json.dumps(dic))


from django.db.backends import utils


def aaa(request):
    return render(request, 'backend/test2.html')
