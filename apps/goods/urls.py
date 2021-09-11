from django.urls import path, include, re_path
from .views import *
from apps.goods.views import IndexView, DetailView, ListView, New_strView, NewDetailView

app_name = 'goods'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),  # 首页
    path("index/", IndexView.as_view(), name="index"),  # 首页
    re_path(r'^goods/(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),  # 详情页
    re_path(r'^list/(?P<type_id>\d+)/(?P<page>\d+)$', ListView.as_view(), name='list'),  # 列表页
    path('newstr/', New_strView.as_view(), name='newstr'),
    path('newdetail/', NewDetailView.as_view(), name='newdetail')
]
