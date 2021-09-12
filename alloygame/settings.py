import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t&cjgq__p+8it4_@71hu2b(%qgzw4sfwrip9y9zhj!letxcnb+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'tinymce',
    'haystack',
    'user',
    'goods',
    'cart',
    'order',
    'ckeditor',  # 将django-ckeditor 注册到该列表中
    'ckeditor_uploader',  # 富文本编译器上传图片的模块
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alloygame.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alloygame.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alloygame',
        'USER': "root",
        'PASSWORD': "123456",
        "HOST": "192.168.1.132",
        "PORT": 3306,
    }
}

# DEFAULT_CONFIG = {
#     'theme': 'advanced',
#     'width': 600,
#     'height': 400,
# }

CKEDITOR_CONFIGS = {
    # 配置名是default时，django-ckeditor默认使用这个配置
    'my_config': {
        # 编辑器的宽高请根据你的页面自行设置
        'width': '800px',
        'height': '500px',
        'image_previewText': ' ',
        'tabSpaces': 4,
        'toolbar': 'Custom',
        # 添加按钮在这里
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'RemoveFormat'],
            ['NumberedList', 'BulletedList'],
            ['Blockquote', 'CodeSnippet'],
            ['Image', 'Link', 'Unlink'],
            ['Maximize']
        ],
        # 插件
        'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'widget', 'lineutils', ]),
    }
}

CKEDITOR_UPLOAD_PATH = ''
AUTH_USER_MODEL = 'user.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 设置图片上传路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# 图片的统一路由
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# smtp服务器地址
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = '25'
# 发送邮件的邮箱
EMAIL_HOST_USER = "hjk1321252@163.com"
# 授权密码
EMAIL_HOST_PASSWORD = 'FZXIQXXOJHZBONGH'
# 收件人看到的发件人
EMAIL_FROM = '合金游戏<hjk1321252@163.com>'

# redis缓存设置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1/9",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# 配置session存储方式
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
# 未登录跳转到指定的地址
LOGIN_URL = '/user/login/'

# 设置Django的文件存储类
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'

# 设置fdfs使用的client.conf文件路径
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置fdfs存储服务器上nginx的IP和端口号
FDFS_URL = 'http://192.168.1.132:8888/'

# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
