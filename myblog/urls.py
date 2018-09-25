from django.contrib import admin
from django.urls import path, include, re_path
from frontend import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', views.home),

    path('study/', views.study_models),
    path('index2/', views.index2),
    path('test/', views.test),
    path('login2/', views.login2),
    path('ajax_login/', views.ajax_login),
    path('pc-geetest/register', views.get_geetest),
    # 注册相关页面
    path('register/', views.register),
    path('check_user/', views.check_user),
    # 获取验证码
    path('auth_code/', views.auth_code),
    path('mem-admin/', include("backend.urls")),   # 后台

    # 用户登录提交的url地址
    path('login/', views.login),
    # 用户注销提交的url地址
    path('logout/', views.logout),
    # 匹配文章详情页对应的具体的文章链接
    path('article/<int:article_id>.html', views.article_detail),
    # 基于tag的访问
    path('tag/<int:tag_id>', views.tag),
    # 当没有匹配任何条件的时候就会匹配到默认的首页
    path('', views.home),
]
