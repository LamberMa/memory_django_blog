import json
import os
import time
import markdown
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.conf import settings
from django.utils.safestring import mark_safe

from utils.auth_code import rd_check_code
from utils import busybox
from backend import models
from frontend import form
from frontend.form import RegisterForm

from geetest import GeetestLib


def home(request):
    article_list = models.Article.objects.all()
    return render(request, 'home.html', {
        'article_list': article_list
    })


# 登录模块
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
            # 如果极验返回的这个result是有内容的，说明验证码验证成功，接下来验证用户个人账号信息
            user = models.User.objects.filter(username=username, password=busybox.get_rand_str(password)).first()
            if user:
                # 用户名密码正确，给用户做登录，将用户的session信息保存到django_session信息中（其实就是数据库中）
                request.session['user'] = {
                    'userid': user.uid,
                    'name': user.username,
                    'nickname': user.nickname,
                }
                # 设置完session以后让用户redirect到根目录
                ret['msg'] = "/"
            else:
                # 当查不到这个用户的时候基本就是用户名或者密码错误了。
                ret['status'] = 1
                ret['msg'] = "用户名或密码错误"
        else:
            # 如果验证码验证失败，那么返回错误信息
            ret['status'] = 1
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)


# 登出模块
def logout(request):
    del request.session['user']
    return redirect('/')


def article_detail(request, article_id):
    article_obj = models.ArticleDetail.objects.filter(article_id=article_id).first()
    md = markdown.Markdown(extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc',])
    article_obj.content = md.convert(article_obj.content)
    article_obj.toc = md.toc
    return render(request, 'frontend/article_detail.html', {
        'article_obj': article_obj,
    })


def tag(request):
    pass


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
        ret = {'status': 1, 'msg': '', 'info': ''}
        obj = RegisterForm(request, request.POST, request.FILES)
        if obj.is_valid():
            # 提交的内容符合要求和规则
            # 这里的avatar其实是一个对象,直接print会把上传文件的文件名打印出来
            # 我这里是多做了一步重命名的操作，其实如果再没设置upload路径的话也是ok的
            # 它会直接在数据库插入这个文件名，如果文件有重名的话会默认在后面拼接一个随机字符串。
            avatar = obj.cleaned_data.get('avatar')
            # 看看用户有没有上传图片，如果上传了就重命名
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
            # 如果用户没有上传图片的话那么就把这个key给pop出来，否则会插入空值
            # pop出来之后会插入字段的默认值，也就是我们设置的默认头像的位置。
            else:
                obj.cleaned_data.pop('avatar')

            obj.cleaned_data.pop('re_password')
            obj.cleaned_data.pop('auth_code')

            try:
                models.User.objects.create(**obj.cleaned_data)
                print('插入成功')
                ret['msg'] = '注册成功！'
                return HttpResponse(json.dumps(ret))
            except Exception as e:
                ret['status'] = 0
                ret['msg'] = '插入数据库有错误'
                print(e)
                return HttpResponse(json.dumps(ret))
        else:
            # 这里采用两种不同的写法，可以使用JsonResponse也可以先用json.dumps然后HTTPResponse
            # JsonResponse本身就是HttpResponse的一个子类
            ret['status'] = 0
            ret['msg'] = obj.errors
            ret_json = json.dumps(ret)
            return HttpResponse(ret_json)


# 检查用户名是否可用的函数
def check_user(request):
    # 1表示帐号是可以使用的，0表示帐号已经被占用了。首先初始化一个空字典
    # 默认发的就是get请求，所以这里也就不做什么判断了。
    ret = {'status': True, 'msg': ''}
    username = request.GET.get('username')
    # 如果用户被占用的话应该可以查到值，如果没有被占用的话应该返回的是一个空的queryset
    is_exist = models.User.objects.filter(username=username)
    if is_exist:
        ret['status'] = False
        ret['msg'] = '用户名已存在'
        return HttpResponse(json.dumps(ret))
    else:
        # ret['msg'] = '用户名尚未注册可以使用'
        return HttpResponse(json.dumps(ret))


def get_geetest(request):

    user_id = 'test'
    gt = GeetestLib(settings.PC_GEETEST_ID, settings.PC_GEETEST_KEY)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


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


def index2(request):
    return render(request, 'frontend/tpl2/index2.html')


def test(request):
    return render(request, 'test.html')


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
