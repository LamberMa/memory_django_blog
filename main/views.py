import json

from django.shortcuts import render, HttpResponse, redirect
from main import models
from main import form


# HomePage
def home(request):
    return render(request, 'home.html')


def study_models(request):
    obj = models.UserType.objects.filter(userinfo__username='齐茂森')
    print(obj)
    obj2 = models.UserType.objects.filter(caption='2B用户').first()
    print(obj2.userinfo_set.all())

    a = 1
    return render(request, 'model.html', {
        'a': a
    })


def login(request):
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


