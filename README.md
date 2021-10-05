# Alloygame


基于`python3.8`和`Django3.2`的游戏资讯平台。


## 主要功能：

- 支持游戏购买，对接支付宝
- 详细的游戏资讯
- 支持发布游戏资讯文章
- 侧边栏功能，最新文章
- 评论功能，发表回复评论
- 支持平台全文搜索
- 支持邮箱注册


## 安装

mysql客户端从`pymysql`修改成了`mysqlclient`，具体请参考 [pypi](https://pypi.org/project/mysqlclient/) 查看安装前的准备。

使用pip安装： `pip install -Ur requirements.txt`

如果你没有pip，使用如下方式安装：

- OS X / Linux 电脑，终端下执行:

    ```
    curl http://peak.telecommunity.com/dist/ez_setup.py | python
    curl https://bootstrap.pypa.io/get-pip.py | python
    ```

- Windows电脑：

  下载 http://peak.telecommunity.com/dist/ez_setup.py 和 https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  这两个文件，双击运行。

## 运行

修改`alloygame/setting.py` 修改数据库配置，如下所示：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alloygame',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 3306,
    }
}
```

### 创建数据库

mysql数据库中执行:

```sql
CREATE
DATABASE `alloygame` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
```

然后终端下执行:

```bash
./manage.py makemigrations
./manage.py migrate
```

**注意：** 在使用 `./manage.py` 之前需要确定你系统中的 `python` 命令是指向 `python 3.6` 及以上版本的。如果不是如此，请使用以下两种方式中的一种：

- 修改 `manage.py` 第一行 `#!/usr/bin/env python` 为 `#!/usr/bin/env python3`
- 直接使用 `python3 ./manage.py makemigrations`

### 创建超级用户

终端下执行:

```bash
./manage.py createsuperuser
```


### 收集静态文件

终端下执行:

```bash

```

### 开始运行：

执行： `./manage.py runserver`

浏览器打开: http://127.0.0.1:8000/  就可以看到效果了。

## 服务器部署

本地安装部署请参考 [alloygame部署教程](#)
有详细的部署介绍.



## 更多配置:

## 问题相关

有任何问题欢迎提Issue,或者将问题描述发送至我邮箱 ``.我会尽快解答.推荐提交Issue方式.

---

## 致大家🙋‍♀️🙋‍♂️

如果本项目帮助到了你，请在[这里]留下你的网址，让更多的人看到。 您的回复将会是我继续更新维护下去的动力。




---

感谢jetbrains
<div>    
<a href="https://www.jetbrains.com/?from=DjangoBlog"><img src="https://resource.lylinux.net/image/2020/07/01/logo.png" width="150" height="150"></a>
</div>
