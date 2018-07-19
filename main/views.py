import json
import os
import time
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import auth

from utils.auth_code import rd_check_code
from main import models
from main import form
from main.form import RegisterForm

from geetest import GeetestLib


def boot(request):
    return render(request, 'boot.html')


def register(request):
    """
    注册相关视图函数
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = RegisterForm(request)
        return render(request, 'register.html', {'obj': obj})
    else:
        # 同时接受用户发过来的数据和文件，我们在这里重新加工了Form类，需要多传递一个request参数
        obj = RegisterForm(request, request.POST, request.FILES)
        if obj.is_valid():
            avatar = obj.cleaned_data.get('avatar')
            if avatar:
                # 拼接存储图片的url路径
                file_name = "%s_%s.%s" % (obj.cleaned_data['username'],
                                          str(time.time()).split('.')[0],
                                          avatar.content_type.split('/')[-1],)
                file_url = os.path.join('static/imgs/head/user', file_name)
                with open(file_url, 'wb') as file_handler:
                    for chunk in avatar.chunks():
                        file_handler.write(chunk)
                obj.cleaned_data['avatar'] = os.path.join('/', file_url)
            else:
                obj.cleaned_data.pop('avatar')

            obj.cleaned_data.pop('re_password')
            obj.cleaned_data.pop('auth_code')
            print(obj.cleaned_data)
            try:
                models.User.objects.create(**obj.cleaned_data)
            except Exception as e:
                print(e)

            return redirect('/')

        return render(request, 'register.html', {'obj': obj})


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


def auth_code(request):
    """
    生成验证码并将生成的图片返回给前端
    :param request: request请求
    :return: 图片的字节流
    """
    img, code = rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['auth_code'] = code
    print(code)
    # 把内存中读取到的图片内容返回就可以了。
    return HttpResponse(stream.getvalue())