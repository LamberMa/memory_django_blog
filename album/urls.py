from django.urls import path, include
from album import views

urlpatterns = [
    path('index/', views.index),
    path('album_json', views.index2)
]