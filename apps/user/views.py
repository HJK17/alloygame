import re
import random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout  # 要加上这句话不然会报错（1）
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired  # 加密

from apps.goods.models import GoodsSKU
from apps.order.models import OrderInfo, OrderGoods
from apps.user.models import User, Address
from celery_tasks.tasks import send_register_active_email, send_verify_code
from utils.image_code.code import verify_code
from utils.mixin import LoginRequireMixin


def register(request):
    """显示注册页面"""
    if request.method == "GET":
        return render(request, "register.html")
    else:
        """注册处理"""
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")  # 同意协议
        if allow != 'on':
            return render(request, "register.html", {'errmsg': "请同意协议"})
        # 数据效验
        if not all([username, password, email]):  # all 方法 可迭代判断每个元素
            return render(request, "register.html", {'errmsg': "数据不完整"})
        # 验证邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, "register.html", {'errmsg': "邮箱错误"})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, "register.html", {'errmsg': "用户名已存在"})
        # 业务处理
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 返回处理
        return redirect(reverse('goods:index'))


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([username, password, cpassword, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户名存在'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # 发邮件
        send_register_active_email.delay(email, username, token)

        return redirect(reverse('goods:index'))


class ActiveView(View):
    """  用户激活  """

    def get(self, request, token):
        """进行用户激活"""
        # token解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取激活用户的id
            user_id = info['confirm']
            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 返回登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse("过期了")


class LoginView(View):
    """登录"""

    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        """登录校验"""
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理:登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后所要跳转到的地址
                # 默认跳转到首页
                next_url = request.GET.get('next', reverse('goods:index'))

                # 跳转到next_url
                response = redirect(next_url)  # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse("goods:index"))


class ChangePassword(View):
    """修改密码"""

    def get(self, request):
        return render(request, 'changepassword.html')

    def post(self, request):
        con = get_redis_connection("default")
        user_name = request.POST.get("user_name")
        code = request.POST.get("code")  # 验证码
        # 上传来的验证码
        img_code = request.POST.get("img_code")  # 图片
        user = User.objects.get(username=user_name)
        password = request.POST.get("password")
        redis_code = con.get(user_name).decode()  # 验证码 decode()将b转出字符串
        csrf_token = request.COOKIES.get("csrftoken")
        # 数据库保存的验证码
        send_img_code = con.get("password_%s" % csrf_token).decode()  # 图片
        con.delete("password_%s" % csrf_token)
        con.delete(user_name)
        print(send_img_code, "   ", img_code)
        print('code', code, 'reds', redis_code)
        if code == redis_code and send_img_code.lower() == img_code:
            user.set_password(password)
            user.save()
            return JsonResponse({"code": 1})

        else:
            return JsonResponse({"code": 2})


class SendCode(View):
    """验证信息"""

    def post(self, request):
        """发送验证邮件"""
        user_name = request.POST.get("user_name")
        user = User.objects.get(username=user_name)
        email = user.email
        user_name = user.username
        token = "".join(random.sample("1234567890", 4))
        # 发送邮件
        send_verify_code(email, user_name, token)
        con = get_redis_connection("default")
        con.set(user_name, token)
        return JsonResponse({"code": 1})


# 图片验证码
class ImageCode(View):
    """验证信息"""

    def get(self, request):
        """发送验证邮件"""
        # 生成验证码图片 名字 真实文本 图片数据
        name, text, image_data = verify_code()
        con = get_redis_connection()
        csrf_token = request.COOKIES.get("csrftoken")
        con.set("password_%s" % csrf_token, text, 300)
        return HttpResponse(image_data, content_type='image/jpg')


class UserInfoView(LoginRequireMixin, View):
    """用户中心 信息页"""

    def get(self, request):
        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(request.user)

        # 获取用户的历史游览记录
        # from redis import StrictRedis
        # sr = StrictRedis(host="192.168.80.132", port=6379, db=9)

        con = get_redis_connection("default")
        history_key = "history_%d" % user.id

        # 获取用户最新游览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)
        # 从数据库中查询用户游览商品的具体信息
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        # 组织上下文
        context = {"page": "user",
                   "address": address,
                   "goods_li": goods_li}
        return render(request, 'user_center_info.html', context)


# /user/order
class UserOrderView(LoginRequireMixin, View):
    """用户中心 订单页"""

    def get(self, request, page):
        # 获取用户的订单信息

        # 获取用户的默认地址信息
        #
        user = request.user
        orders = OrderInfo.objects.filter(user=user, is_delete=0).order_by("-create_time")

        # 遍历获取订单商品的信息
        for order in orders:
            # 根据order_Id 查询订单商品信息
            order_skus = OrderGoods.objects.filter(order_id=order.order_id)
            # 遍历order_skus计算商品小计
            for order_sku in order_skus:
                # 计算小计
                amount = order_sku.count * order_sku.price
                # 动态给order_sku增加属性 保存订单商品小计
                order_sku.amount = amount
            # 保存订单状态标题
            order.status_name = OrderInfo.ORDER_STATUS[order.order_status]
            # 动态给order增加属性
            order.order_skus = order_skus
        # 分页
        paginator = Paginator(orders, 1)
        try:
            page = int(page)
        except Exception as e:
            page = 1
        if page > paginator.num_pages:
            page = 1
        order_page = paginator.page(page)
        # 获取page页的内容
        # 1 总页数小于五页 页面上显示所有页码
        # 2 如果当前页是前三页 显示前五页的页码
        # 3 如果当前页是后三页 显示后五页的页码
        # 4 其他情况 显示当前页,当前页的前两页和后两页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)
        # 组织上下文
        if len(orders) == 0:
            pages = None
        context = {
            'order_page': order_page,
            'pages': pages,
            'page': orders,
        }
        return render(request, 'user_center_order.html', context)


# /user/address
class UserAddressView(LoginRequireMixin, View):
    """用户中心-地址页"""

    def get(self, request):
        """显示"""
        # 获取登录用户对应User对象
        user = request.user

        # 获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True)  # models.Manager
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None
        address = Address.objects.get_default_address(user)

        # 使用模板
        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        """地址的添加"""
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all([receiver, addr, phone, type]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        address = Address.objects.get_default_address(user)
        # 新增一个地址  原有  则为false
        if address:
            is_default = False
        else:
            is_default = True

        # 添加地址
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('user:address'))  # get请求方式


from apps.goods.models import ArticleCategory, Article


class WriteView(LoginRequiredMixin, View):

    def get(self, request):
        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        context = {
            'categories': categories
        }
        return render(request, 'write.html', context=context)

    def post(self, request):
        # 接收数据
        avatar = request.FILES.get('avatar')
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        tags = request.POST.get('tags')
        sumary = request.POST.get('sumary')
        content = request.POST.get('content')
        user = request.user

        # 验证数据是否齐全
        if not all([avatar, title, category_id, sumary, content]):
            return HttpResponseBadRequest('参数不全')

        # 判断文章分类id数据是否正确
        try:
            article_category = ArticleCategory.objects.get(id=category_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseBadRequest('没有此分类信息')

        # 保存到数据库
        try:
            article = Article.objects.create(
                author=user,
                avatar=avatar,
                category=article_category,
                tags=tags,
                title=title,
                sumary=sumary,
                content=content
            )
        except Exception as e:
            return HttpResponseBadRequest('发布失败，请稍后再试')

        # 返回响应，跳转到文章详情页面
        # 暂时先跳转到首页
        return redirect(reverse('goods:newstr'))


from django.http import HttpResponseNotFound


class MynewstrView(LoginRequireMixin, View):
    def get(self, request):
        id = request.GET.get('id')
        cat_id = request.GET.get('cat_id', 1)
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)
        # 判断分类id
        try:
            category = ArticleCategory.objects.get(id=cat_id)
        except ArticleCategory.DoesNotExist:
            return HttpResponseNotFound('没有此分类')

        # 获取博客分类信息
        categories = ArticleCategory.objects.all()

        article = Article.objects.filter(
            id=id
        )
        article.delete()

        # 分页数据
        articles = Article.objects.filter(
            category=category
        )

        # 创建分页器：每页N条记录
        paginator = Paginator(articles, page_size)
        # 获取每页商品数据
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # 如果没有分页数据，默认给用户404
            return HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        context = {
            'categories': categories,
            'category': category,
            'articles': page_articles,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num,
        }
        return render(request, 'mynewstr.html', context)

    # def post(self, request):
    #     """删除文章功能"""
    #
    #     print('id--->', id)
    #
    #     return render(request, 'mynewstr.html')
