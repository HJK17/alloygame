from django.urls import re_path, path
from apps.order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView, CommentView, OrderDelete

app_name = 'order'

urlpatterns = [
    path('place', OrderPlaceView.as_view(), name='place'),  # 提交订单页面显示
    path('commit', OrderCommitView.as_view(), name='commit'),  # 创建订单
    path('pay', OrderPayView.as_view(), name='pay'),  # 订单支付
    path('check', CheckPayView.as_view(), name='check'),  # 查询交易支付情况
    re_path(r'^comment/(?P<order_id>.+)/$', CommentView.as_view(), name='comment'),  # 验证支付
    re_path(r'^delete/$', OrderDelete.as_view(), name='delete'),  # 删除订单

]
