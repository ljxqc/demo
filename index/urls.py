from django.urls import path, re_path
from . import views



urlpatterns = [
    path('', views.index),
    path('<year>/<int:month>/<slug:day>', views.mydate),  # 带变量的 URL
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/', views.mydate),  # 带正则的URL
    # re_path('(?P<year>[0-9]{4})/', views.myyear, name='myyear'),  # 带名字的URL，可作HTML反向解析
    re_path('dict/(?P<year>[0-9]{4})/', views.myyear_dict, {'month': '05'}, name='myyear_dict', ),  # 设置额外参数（字典）
]