from django.contrib import admin
from django.urls import path, include, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path("cart/", include("cart.urls")),
    path('order/', include('order.urls')),  # 订单模块
    re_path(r"^", include("goods.urls")),
    # re_path(r"^tinymce/", include("tinymce.urls")),  # 富文本编辑器
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', include('haystack.urls')),  # 全文检索框架
]
