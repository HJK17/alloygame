from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings


class GoodsType(BaseModel):
    '''商品类型模型类'''
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')

    class Meta:
        db_table = 'ag_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):
    '''商品SKU模型类'''
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    type = models.ForeignKey('GoodsType', verbose_name='商品种类', on_delete=models.CASCADE)
    goods = models.ForeignKey('Goods', verbose_name='商品SPU', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    imgvideo = models.ImageField(upload_to='goods', verbose_name='视频略缩图')
    video = models.FileField(upload_to="goods", null=True, blank=True, verbose_name="视频内容")  # 视频
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='商品状态')

    # 应该加上这步，表示显示时返回的是自定义信息，而不是 object 形式
    def __str__(self):  # __str__ on Python 3
        return self.name

    class Meta:
        db_table = 'ag_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    '''商品SPU模型类'''
    name = models.CharField(max_length=50, verbose_name='商品SPU名称')
    # 富文本类型:带有格式的文本
    detail = HTMLField(blank=True, verbose_name='商品详情')
    # new = RichTextUploadingField(blank=True, verbose_name='商品新闻')
    #  = HTMLField(blank=True, verbose_name='商品攻略')
    new = RichTextUploadingField(config_name='my_config', blank=True, verbose_name='商品新闻')
    strategy = RichTextUploadingField(config_name='my_config', blank=True, verbose_name='商品攻略')

    class Meta:
        db_table = 'ag_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "goods" + self.name


class GoodsImage(BaseModel):
    '''商品图片模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')

    class Meta:
        db_table = 'ag_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class GoodsImgvideo(BaseModel):
    '''略缩图型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=models.CASCADE)
    imgvideo = models.ImageField(upload_to='goods', verbose_name='略缩图路径')

    class Meta:
        db_table = 'ag_goods_imgvideo'
        verbose_name = '视频略缩图'
        verbose_name_plural = verbose_name


class GoodsVideo(BaseModel):
    '''商品视频模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=models.CASCADE)
    video = models.ImageField(upload_to='goods', verbose_name='视频路径')

    class Meta:
        db_table = 'ag_goods_video'
        verbose_name = '商品视频'
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    '''首页轮播商品展示模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'ag_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name


class IndexTypeGoodsBanner(BaseModel):
    '''首页分类商品展示模型类'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型', on_delete=models.CASCADE)
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU', on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    def __str__(self):
        return self.sku.name

    class Meta:
        db_table = 'ag_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.CharField(max_length=256, verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        db_table = 'ag_index_promotion'
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


from django.db import models
from django.utils import timezone


# Create your models here.
class ArticleCategory(models.Model):
    """
    文章分类
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tb_category'
        verbose_name = '类别管理'
        verbose_name_plural = verbose_name


from apps.user.models import User


class Article(models.Model):
    """
    文章
    """
    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一起
    # 参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 文章栏目的 “一对多” 外键
    category = models.ForeignKey(
        ArticleCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    # 文章标签
    tags = models.CharField(max_length=20, blank=True)
    # 文章标题。
    title = models.CharField(max_length=100, null=False, blank=False)
    # 概要
    sumary = models.CharField(max_length=200, null=False, blank=False)
    # 文章正文。
    # content = models.TextField()
    content = RichTextUploadingField(config_name='my_config')
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章点赞数
    comments_count = models.PositiveIntegerField(default=0)
    # 文章创建时间。
    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间。
    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
        db_table = 'tb_article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 将文章标题返回
        return self.title


class Comment(models.Model):
    # 评论内容
    content = models.TextField()
    # 评论的文章
    article = models.ForeignKey(Article,
                                on_delete=models.SET_NULL,
                                null=True)
    # 发表评论的用户
    user = models.ForeignKey('user.User',
                             on_delete=models.SET_NULL,
                             null=True)
    # 评论发布时间
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name
