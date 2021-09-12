from django.urls import path, include, re_path
from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, \
    UserAddressView, ChangePassword, SendCode, ImageCode, WriteView, MynewstrView

app_name = 'user'

urlpatterns = [
    re_path(r"^register/$", RegisterView.as_view(), name='register'),  # 注册
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 激活
    # path('login', LoginView.as_view(), name='login'),  # 登录
    re_path(r"^login/$", LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name='logout'),  # 登出
    path('change_password/', ChangePassword.as_view(), name='ChangePassword'),  # 修改密码
    path('send_code/', SendCode.as_view(), name='SendCode'),  # 修改密码
    path('ImageCode/', ImageCode.as_view(), name='ImageCode'),  # 验证码图片

    path('', UserInfoView.as_view(), name='user'),  # 用户中心--信息页
    re_path(r"^order/(?P<page>\d+)/$", UserOrderView.as_view(), name='order'),
    path('address', UserAddressView.as_view(), name='address'),  # 用户中心--地址页

    path('write/', WriteView.as_view(), name='write'),  # 写文章
    path('mynewstr/', MynewstrView.as_view(), name='mynewstr')  # 我的文章



]
