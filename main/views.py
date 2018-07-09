import json

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from main import models
from main import form
from main.form import RegisterForm
from geetest import GeetestLib
from django.conf import settings
from django.contrib import auth


def get_geetest(request):

    user_id = 'test'
    gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login(request):
    if request.method == "POST":
        # 初始化一个字典用于给ajax请求返回数据
        ret = {'status': 0, 'msg': ''}
        # 从请求中获取到用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 获取极验活动验证码相关参数
        gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 如果极验返回的这个result是有内容的，说明验证成功
            user = auth.authenticate(username=username, password=password)
            if user:
                # 用户名密码正确，给用户做登录
                auth.login(request, user)
                ret['msg'] = "/index/"
            else:
                # 用户名密码错误
                ret['status'] = 1
                ret['msg'] = "用户名或密码错误"
        else:
            ret['status'] = 1
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)


def register(request):

    if request.method == 'GET':
        obj = RegisterForm()
        return render(request, 'register.html', {'obj': obj})
    else:
        obj = RegisterForm(request.POST)
        if obj.is_valid():
            pass
        return render(request, 'register.html', {'obj': obj})


def study_models(request):
    obj = models.UserType.objects.filter(userinfo__username='齐茂森')
    print(obj)
    obj2 = models.UserType.objects.filter(caption='2B用户').first()
    print(obj2.userinfo_set.all())

    a = 1
    return render(request, 'model.html', {
        'a': a
    })


def login2(request):
    if request.method == 'GET':
        obj = form.LoginForm()
        return render(request, 'login.html', {'obj': obj})
    else:
        obj = form.LoginForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            return redirect('https://www.baidu.com')
        else:
            print(obj.errors)
            print(obj.errors['username'])
            # 拿多个错误信息的第一个，只要错误信息没满足就有问题，我们永远拿第一个就行了
            # print(obj.errors['password'][0])
            return render(request, 'login.html', {
                'obj': obj
            })


def ajax_login(request):
    ret = {
        'status': True,
        'msg': None
    }
    if request.method == "POST":
        obj = form.LoginForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
        else:
            print(obj.errors)
            ret['status'] = False
            ret['msg'] = obj.errors
    v = json.dumps(ret)
    # return render(request, )
    return HttpResponse(v)


# HomePage
def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')


def home(request):
    return render(request, 'home.html')


def backend(request):
    return render(request, 'backend.html')
