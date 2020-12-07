# demo
A repository of learning

# 什么是 Django ?

Django 是一款基于 Python 语言的开源 web 框架，采用 MTV 的框架模式，即：

- Model：模型；数据存取层，处理与数据相关的所有事务
- Template：模板；
- Views：视图

# Web 框架原理

理解：所有的 Web 应用本质上是一个 socket 服务端，而浏览器是一个 socket 客户端。

### 自定义 web 框架：

基于 socket 实现一个简单 web

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()

while True:
    conn, addr = s.accept() #客户端socket对象 客户端地址
    data = conn.recv(8096)  #接收浏览器发来的消息
    print(conn)
    print(addr)
    print(data)
    conn.send(b'OK!') #只能发送字节
    conn.close()
```

访问 `127.0.0.1:80` 后浏览器显示：

![image-20201111111023751](https://ljxqc.github.io/demo/raw/images/image-20201111111023751.png)

打印输出：

```python
<socket.socket fd=716, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 80), raddr=('127.0.0.1', 13848)>
('127.0.0.1', 13848)
b'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n\r\n'
```

浏览器发的消息具有一定的格式，即必须符合 HTTP 协议

HTTP，即超文本传输协议（英文：**H**yper**T**ext **T**ransfer **P**rotocol）是一种用于分布式、协作式和超媒体信息系统的应用层协议。HTTP是万维网的数据通信的基础。

 HTTP是一个客户端终端（用户）和服务器端（网站）请求和应答的标准（TCP）

每个 HTTP 请求和响应都应遵循相同的格式，一个 HTTP 包含 Header 和 Body 两部分， 其中 Body 是可选的。HTTP 响应中的 Header  中有一个 `Content-Type` 表命响应的内容格式。如 `text/html` 表示 HTML 网页

HTTP GET 请求的格式

![img](https://images2018.cnblogs.com/blog/867021/201803/867021-20180330221943115-1291906159.png)

HTTP 响应的格式

![img](https://images2018.cnblogs.com/blog/867021/201803/867021-20180330222031912-1851965755.png)

为框架添加 HTTP 协议

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()


while True:
    conn, addr = s.accept() #客户端socket对象 客户端地址
    data = conn.recv(8096)  #接收浏览器发来的消息
    print(data)
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
    conn.send(b'OK!')
    conn.close()
```

### 自定义 web 框架：基于不同路径返回不同的内容

按照 HTTP 协议，客户端发来的消息需要按照一定的格式，通过这些固定格式，可以获取请求方法、url

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()


while True:
    conn, addr = s.accept()
    data = conn.recv(8096)  # 接收客户端发来消息
    data = str(data, encoding='utf-8')  #将字节转为字符串
    url = data.split('\r\n')[0].split()[1] # 获取路由
    if url == '/index':
        response = b'index'
    elif url == '/home':
        response = b'home'
    else:
        response = b'404 Not Found!'
    conn.send(response)
    conn.close()
```

### 自定义 web 框架：基于不同路径返回不同的内容 - - 函数版

路径不同时调用不同的函数

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()

def index(url):
    mse = f'这是一个 {url} 页面'
    return bytes(mse, encoding='utf8')

def home(url):
    mse = f'这是一个 {url} 页面'
    return bytes(mse, encoding='utf8')

while True:
    conn, addr = s.accept()
    data = conn.recv(8096)  # 接收客户端发来消息
    data = str(data, encoding='utf-8')  #将字节转为字符串
    conn.send(b'HTTP/1.1 200 OK\r\n')
    url = data.split('\r\n')[0].split()[1]
    if url == '/index':
        response = index(url)
    elif url == '/home':
        response = home(url)
    else:
        response = b'404 Not Found!'
    conn.send(response)
    conn.close()
```

###  自定义 web 框架：基于不同路径返回不同的内容 - - 函数进阶版

如果路由很多，你会进行很多条件判断。为了优化条件判断，建立一个 路由-调用函数对照表

> list1 = [
>  ('/index', index),
>  ('/home', home)
> ]

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()

def index(url):
    mse = f'这是一个 {url} 页面'
    return bytes(mse, encoding='utf8')

def home(url):
    mse = f'这是一个 {url} 页面'
    return bytes(mse, encoding='utf8')


list1 = [
    ('/index', index),
    ('/home', home)
]

while True:
    conn, addr = s.accept()
    data = conn.recv(8096)  # 接收客户端发来消息
    data = str(data, encoding='utf-8')  #将字节转为字符串
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
    url = data.split('\r\n')[0].split()[1]
    func = None
    for i in list1:
        if i[0] == url:
            func = i[1]
    if func:
        response = func(url)
    else:
        response = b'404 not found'
    conn.send(response)
    conn.close()
```

### 自定义 web 框架：返回完整的 HTML 页面

服务器向浏览器发送的是字节流数据，读取html页面，并将其转化为字节流

定义 index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>INDEX</title>
</head>
<body>
这是一个 INDEX DEMO 页面 ！
</body>
</html>
```

定义 home.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HOME</title>
</head>
<body>
这是一个 HOME DEMO 页面！
</body>
</html>
```

读取 HTML 转化为字节

```python
import socket

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()

def index(url):
    # 读取页面并转化为字节
    with open('index.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    return bytes(msg, encoding='utf8')

def home(url):
    with open('home.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    return bytes(msg, encoding='utf8')


list1 = [
    ('/index', index),
    ('/home', home)
]

while True:
    conn, addr = s.accept()
    data = conn.recv(8096)  # 接收客户端发来消息
    data = str(data, encoding='utf-8')  #将字节转为字符串
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
    url = data.split('\r\n')[0].split()[1]
    func = None
    for i in list1:
        if i[0] == url:
            func = i[1]
            break
    if func:
        response = func(url)
    else:
        response = b'404 not found'
    conn.send(response)
    conn.close()
```

浏览器访问 `127.0.0.1/index`

![image-20201111140325805](MyDjango\images\image-20201111140325805.png)

### 自定义 Web 框架：返回动态的 HTML 页面

上面是一个静态的网页，我们可以通过 **字符串替换** 返回一个静态的网页

index.html 中定义好待替换的字符：例如 ###

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>INDEX</title>
</head>
<body>
这是一个 INDEX DEMO 页面 ！
当前时间为：###
</body>
</html>
```

服务器字符串替换

```python
import socket
import time

s = socket.socket()
s.bind(('127.0.0.1', 80))
s.listen()

def index(url):
    with open('index.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    now = time.time()
    msg = msg.replace('###', str(now))  #字符串替换 ###
    print(msg)
    return bytes(msg, encoding='utf8')

def home(url):
    with open('home.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    return bytes(msg, encoding='utf8')


list1 = [
    ('/index', index),
    ('/home', home)
]

while True:
    conn, addr = s.accept()
    data = conn.recv(8096)  # 接收客户端发来消息
    data = str(data, encoding='utf-8')  #将字节转为字符串
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
    url = data.split('\r\n')[0].split()[1]
    func = None
    for i in list1:
        if i[0] == url:
            func = i[1]
            break
    if func:
        response = func(url)
    else:
        response = b'404 not found'
    conn.send(response)
    conn.close()
```

浏览器访问 `127.0.0.1/index`

![image-20201111141145079](D:\MyDjango\images\image-20201111141145079.png)

### 自定义 Web 框架：基于 WSGI

对于真实开发的 python web 程序来说，一般会分为两个部分：

- 服务器程序
- 应用程序

服务器程序负责对 socket 服务器进行封装，并在请求到来时，对请求的数据进行整理

应用程序负责具体的逻辑处理，为了方便应用程序的开发，就出现了众多的Web框架，例如：Django、Flask、web.py 等。不同的框架有不同的开发方式，但是无论如何，开发出的应用程序都要和服务器程序配合，才能为用户提供服务。

而服务器程序就需要为不同的框架提供不同的支持，这样混乱的局面无论对于服务器还是框架，都是不好的

这时候，标准化就变得尤为重要。我们可以设立一个标准，只要服务器程序支持这个标准，框架也支持这个标准，那么他们就可以配合使用。一旦标准确定，双方各自实现。这样，服务器可以支持更多支持标准的框架，框架也可以使用更多支持标准的服务器。

WSGI（Web Server Gateway Interface）就是一种规范，它定义了使用Python编写的web应用程序与web服务器程序之间的接口格式，实现web应用程序与web服务器程序间的解耦

常用的WSGI服务器有uwsgi、Gunicorn。而Python标准库提供的独立WSGI服务器叫wsgiref，Django开发环境用的就是这个模块来做服务器。

利用 wsgiref 替换 web 框架的 socket server 部分

```python
import time
from wsgiref.simple_server import make_server


def index(url):
    with open('index.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    now = time.time()
    msg = msg.replace('###', str(now))
    return bytes(msg, encoding='utf8')

def home(url):
    with open('home.html', 'r', encoding='utf-8') as f:
        msg = f.read()
    return bytes(msg, encoding='utf8')


list1 = [
    ('/index', index),
    ('/home', home)
]

def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])  #设置HTTP响应的状态码及头信息
    url = environ['PATH_INFO']  #取到用户输入的url
    func = None
    for i in list1:
        if i[0] == url:
            func = i[1]
            break
    if func:
        response = func(url)
    else:
        response = b'404 not found'
    return [response, ]

if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 80, run_server)
    httpd.serve_forever()
```

### 自定义 Web 框架：利用 jinjia2 进行模板数据渲染

利用现场的模板渲染工具：

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>INDEX</title>
</head>
<body>
这是一个 INDEX DEMO 页面 ！

<h1>姓名：{{ name }}</h1>
<h1>爱好：</h1>
<ul>
    {% for hobby in hobby_list %}
    <li>{{ hobby }} </li>
    {% endfor %}
</ul>
</body>
</html>
```

服务端：

```python
from wsgiref.simple_server import make_server
from jinja2 import Template

def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        data = f.read()
    # 利用 jiaji2 模板渲染
    template = Template(data)
    ret = template.render({'name': "Alex", "hobby_list": ["烫头", "泡吧"]})
    return [bytes(ret, encoding='utf8'), ]

def home():
    with open('home.html', 'rb') as f:
        data = f.read()
    return [data, ]


list1 = [
    ('/index', index),
    ('/home', home)
]

def run_server(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html;charset=utf8'), ])  #设置HTTP响应的状态码及头信息
    url = environ['PATH_INFO']  #取到用户输入的url
    func = None
    print(url)
    for i in list1:
        if i[0] == url:
            func = i[1]
            break
    if func:
        return func()
    else:
        return [bytes("404没有该页面", encoding="utf8"), ]


if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 80, run_server)
    httpd.serve_forever()
```

浏览器访问 127.0.0.1/index

![image-20201111164620920](D:\MyDjango\images\image-20201111164620920.png)



# 安装 Django

> pip install django

# 创建 Django 项目

## 1、利用 Pycharm 创建 Django 项目

1、菜单栏 - File - New Project

![image-20200710171341770](D:\MyDjango\images\image-20200710171341770.png)

2、

![image-20200710172836794](D:\MyDjango\images\image-20200710172836794.png)

## 2、利用 CMD 创建 Django 项目

#### 1、创建虚拟环境

命令行创建：

> python -m venv env

激活：

> cd env/Scripts

> activate.bat

激活后：

![image-20201112142003253](D:\MyDjango\images\image-20201112142003253.png)

虚拟环境安装 django

> pip install django

#### 2、创建 Django 项目

虚拟环境激活情况下：

> cd e:

> django-admin startproject MyDjango

创建 app

> cd MyDjango

> python manage.py startapp index

创建后 文件目录

![image-20201112144040060](D:\MyDjango\images\image-20201112144040060.png)

启动项目：

cmd 命令行，在项目目录下运行：

> python manage.py runserver 80

![image-20201112144514054](D:\MyDjango\images\image-20201112144514054.png)

浏览器访问：`127.0.0.1:80`

![image-20201112144547962](D:\MyDjango\images\image-20201112144547962.png)

# Django 配置信息

项目配置是根据实际开发需求从而对整个Web框架编写相关配置信息。配置信息主要由项目的settings.py实现，主要配置有项目路径、密钥配置、域名访问权限、App列表、配置静态资源、配置模板文件、数据库配置、中间件和缓存配置

### 基本配置信息

一个简单的项目必须具备的基本配置信息有：项目路径、密钥配置、域名访问权限、App列表和中间件

```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # 项目路径


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')mm8s71l7a!budx)5^j+61%css416=sg_!flz^tmh-pu)9c(39'  # 密钥配置

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 调试模式

ALLOWED_HOSTS = []  # 域名访问权限


# Application definition
# App 列表
INSTALLED_APPS = [
    'django.contrib.admin',  # 内置后台管理系统
    'django.contrib.auth',  # 内置的用户认证系统
    'django.contrib.contenttypes',  # 记录项目中所有的 model 元数据（Django的ORM框架）
    'django.contrib.sessions',  # session 会话功能
    'django.contrib.messages',  # 消息提示功能
    'django.contrib.staticfiles',  #查找静态资源路径
    'index',  # app
]

```

- BASE_DIR：项目路径，当前项目在系统的具体目录
- SECRET_KET：项目创建自动生成的随机值，用于用户密码、CSRF机制、会话 Sission 数据加密
- DEBUG：调试模式 。开发调试阶段应设为 True，开发调试过程中会自动检测代码是否发生更改，并根据检测结果执行是否刷新重启系统；项目上线时应设为 False
- ALLOWED_LISTS：域名访问权限，设置可访问的域名。DEBUG为True并且ALLOWED_HOSTS为空时，项目只允许以localhost或127.0.0.1在浏览器上访问。当DEBUG为False时，ALLOWED_HOSTS为必填项，否则程序无法启动，如果想允许所有域名访问，可设置ALLOW_HOSTS=['*']。
- INSTALLED_APPS：告诉 Django 有哪些 App。项目创建了 App，须在其中添加 App 名称

### 静态资源配置

静态资源指的是网站中不会改变的文件。在一般的应用程序中，静态资源包括CSS文件、JavaScript文件以及图片等资源文件

静态文件的存放主要由配置文件settings.py设置

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'  # 静态资源访问路由

# 静态文件目录
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # 根目录下的静态文件目录
#     os.path.join(BASE_DIR, 'index/static'),  # app 下的静态文件目录
# ]

# 静态资源根目录，部署时收集整个项目的静态资源，构建静态资源与服务器的映射
# STATIC_ROOT = os.path.join(BASE_DIR, 'all_static')
```

当项目启动时，Django 会根据静态资源存放路径去查找相关的资源文件，查找功能主要由 App 列表 INSTALLED_APPS 的 staticfiles 实现。

这里需注意：

- STATIC_URL：静态资源起始 url，该属性必须配置且不能为空。浏览器访问静态资源时，静态资源的上级目录必须为该属性值。如果没有配置  STATICFILES_DIRS ，STATIC_URL 只能识别 App 里的 static 静态资源，且静态资源文件命名必须为 `static`
- STATICFILES_DIRS：静态资源目录，可选配置。属性值为列表或元组形式，每个元素代表一个静态资源文件夹，这些文件夹可自行命名
- 浏览器访问项目静态资源时，无论静态资源文件如何命名，访问时静态资源的上级目录必须为 STATIC_URL 属性值
- 静态资源的查找顺序为：先按 STATICFILES_DIRS 配置顺序查找，找不到再按照 INSTALLED_APPS 配置顺序查找

### 模板路径配置

在Web开发中，模板是一种较为特殊的HTML文档。这个HTML文档嵌入了一些能够让Python识别的变量和指令，然后程序解析这些变量和指令，生成完整的HTML网页并返回给用户浏览。模板是Django里面的MTV框架模式的T部分，配置模板路径是告诉Django在解析模板时，如何找到模板所在的位置

```python
TEMPLATES = [
    {
         # 模板引擎，内置的模板引擎有DjangoTemplates和jinja2.Jinja2
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        # 设置模板所在路径
        'DIRS': [
            BASE_DIR / 'templates',  # 根目录，用于存放各 app 共用的模板文件
            BASE_DIR / 'index/templates',  # app 模板目录，存放app需要使用的模板文件
                 ],  

        'APP_DIRS': True,  # 是否在app中查找模板文件
        # 用于填充在 RequestContext 中上下文的调用函数，一般情况下不做任何修改
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

```

在项目 根目录 及 App 根目录 创建 templates 模板

根目录 templates 通常存放共用的模板文件，能够供各个 App 的模板文件调用，实现代码的重用

App 目录下的 templates 是存放 当前 app 所需要使用的模板文件



### 数据库配置

数据库配置时选择项目所使用的数据库的类型，不同的数据库需要设置不同的数据库引擎，数据库引擎用于实现项目与数据库的连接，Django 提供四种数据库引擎

- django.db.backends.sqlite3
- django.db.backends.mysql
- django.db.backends.postgresql
- django.db.backends.oracle

项目创建时默认使用 sqlite3 数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
```

使用 mysql 数据库时需安装 mysqlclient 模块

mysqlclient 模块需大于一定的版本，如果发现 mysqlclient 版本大于 Django 版本要求但仍提示 mysqlclient 版本过低，可修改 `django.db.backends.mysql.base`文件中的 

```python
version = Database.version_info
if version < (1, 4, 0):
    raise ImproperlyConfigured('mysqlclient 1.4.0 or newer is required; you have %s.' % Database.__version__)

```

Mysql 数据库配置信息：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'django_db',  # 数据库名
        'USER': 'root',  # 用户
        'PASSWORD': '1234',  # 密码
        'HOST': '127.0.0.1',  # 数据库地址
        'PORT': '3306',  # 数据库端口
    },
}
```

如果 Mysql 版本大于 5.7，Django 连接 Mysql 数据库时会提示 `django.db.utils.OperationalError` 的错误信息，这是由于 Mysql 8.0 密码加密方式发生了改变，8.0 版本用户密码采用的时 cha2 加密方法。

为解决这个问题可通过 sql 语句将 8.0 版本的加密方法改回源来的加密方式

```mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH msyql_native_password BY 'newpassword';
FLUSH PRIVILEGES;
```

如果项目需要配置多个数据库：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Django 提供4种数据库引擎
        # 'ENGINE': 'django.db.backends.mysql',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.oracle',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 设置多个数据库，添加多个字典键值对
    'MyDjango': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'django_db',  # 数据库名
        'USER': 'root',  # 用户
        'PASSWORD': '1234',  # 密码
        'HOST': '127.0.0.1',  # 数据库地址
        'PORT': '3306',  # 数据库端口
    },
}
```



### 中间件配置

中间件（Middleware）是处理 Django 的 请求（request）和 响应（response）对象的钩子

从请求到响应的过程中，当Django接收到用户请求时，Django 首先经过中间件处理请求信息，执行相关的处理，然后将处理结果返回给用户，中间件执行流程如图

![image-20201112180248624](D:\MyDjango\images\image-20201112180248624.png)

开发者可根据自己的开发需求自定义中间件，只要将自定义的中间件添加到配置属性 MIDDLEWARE 中即可激活

```python
# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 内置安全机制，保护用户与网站的通信安全
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话 Session 功能
    'django.middleware.locale.LocaleMiddleware',  # 使用中文
    'django.middleware.common.CommonMiddleware',  # 处理请求信息，规范化请求内容
    'django.middleware.csrf.CsrfViewMiddleware',  # 开启 CSRF 防护功能
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 开启内置的用户认证系统
    'django.contrib.messages.middleware.MessageMiddleware',  # 开启内置的信息提示功能
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 防止恶意程序点击挟持
]
```

配置属性MIDDLEWARE的数据格式为列表类型，每个中间件的设置顺序是固定的，如果随意变更中间件很容易导致程序异常

# 编写 URL 规则

URL（Uniform Resource Locator，统一资源定位符）是对可以从互联网上得到的资源位置和访问方法的一种简洁的表示，是互联网上标准资源的地址。互联网上的每个文件都有一个唯一的URL，用于指出文件的路径位置。简单地说，URL就是常说的网址，每个地址代表不同的网页，在Django中，URL也称为URLconf。

### URL 编写规则

为符合开发规范，每个 App 中都应有一个路由配置文件，即 url.py

所有属于 App 的 url 都应写到对应 App 的路由文件 url.py 中

根目录下的路由文件 url.py 统一管理所有 app 的路由文件。

根目录路由配置

```python
from django.contrib import admin  # 导入admin 功能模块
from django.urls import path, include  # 导入url编写模块

urlpatterns = [
    path('admin/', admin.site.urls),  # 设定admin的URL
    path('', include('index.urls')),  # 将域名路由分发给 index.urls 处理
    path('user/', include('user.urls')),  #将路由 user/ 分发给 user.ursl 处理
]
```

App 路由配置

```python
from django.urls import path,
from . import view   # 导入视图处理模块

urlpatterns = [
    path('', view.index)  # 表示该路由交给 views.index 函数处理
]
```

视图函数 views 中定义 index 函数

```python
from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request, *args, **kwargs):
    return HttpResponse('Hello world ! This Is A Index Page !')
```

浏览器访问 127.0.0.1:8000

![image-20201113174125913](D:\MyDjango\images\image-20201113174125913.png)



### 带变量的 URL

在日常开发中，有时候一个 URL 可以代表多个不同的页面，如编写带有日期的 URL，开发者编写365个不同的URL才能实现，这种做法明显是不可取的。因此，Django在编写URL时，可以对URL设置变量值，使URL具有多样性。

URL 变量类型：

- 字符类型：匹配任何非空字符串，但不包括斜杠；未指定类型时，默认为该类型
- 整型：匹配 0 和正整数
- slug：可理解为注释、后缀或附属等概念，常作为URL的解释性字符。可匹配任何ASCII字符以及连接符和下画线，能使URL更加清晰易懂。比如网页的标题是“13岁的孩子”，其URL地址可以设置为“13-sui-de-hai-zi”。
- uuid：匹配一个uuid格式的对象。为了防止冲突，规定必须使用破折号并且所有字母必须小写，例如075194d3-6885-417e-a8a8-6c931e272f00。

在 URL 中使用 `<>` 添加变量，其中以 `:` 区分类型变量类型和变量名，`:` 前表示变量类型，`:`后表示变量名

在 index.urls 中添加变量

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),  # 表示该路由交给 views.index 函数处理
    path('<year>/<int:month>/<slug:day>', views.mydate),  # 设置变量
]
```

views.mydate

```python
from django.shortcuts import render, HttpResponse

# Create your views here.

def mydate(request, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day))
```

浏览器访问

![image-20201113175238465](D:\MyDjango\images\image-20201113175238465.png)

### URL 中引入 正则表达式

Django 中 re_path 模块 可以向 URL 中引入正则表达式，正则表达式可以对 URL 进行截取和判断

路由中 配置

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),  # 表示该路由交给 views.index 函数处理
    path('<year>/<int:month>/<slug:day>', views.mydate),
    re_path('(?P<year>[0-9]{4})/(?P<month>[0-9]{2}])/(?P<day>[0-9]{2})/', views.mydate),
]
```



### 设置参数 name

参数name的作用是对URL地址进行命名，然后在HTML模板中使用可以生成相应的URL信息。在URL中设置参数name，只要参数name的值不变，无论URL地址信息如何修改都无须修改模板中标签a的href属性值。

app 路由：

```python 
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),  # 表示该路由交给 views.index 函数处理
    re_path('(?P<year>[0-9]{4})/', views.myyear, name='myyear'),  # 带名字的URL，可作HTML反向解析 
]
```

views

```python
from django.shortcuts import render, HttpResponse

# Create your views here.

def myyear(request, year):
    return render(request, 'myyear.html')
```

myyear.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div><a herf="/2018.html">2018 old Archiver</a></div>
<div><a herf="{% url 'myyear' 2018 %}">2018 new Archiver</a></div>
</body>
</html>
```

利用 URL 的 name ，在页面中进行反向解析，无论 URL 路由变成什么，页面中的 href 属性一直不变。

访问 http://127.0.0.1:8000/2020/

![image-20201116155230655](D:\MyDjango\images\image-20201116155230655.png)

访问 http://127.0.0.1:8000/2018/

![image-20201116155307229](D:\MyDjango\images\image-20201116155307229.png)



### 设置额外参数

URL 中还可以设置额外参数，设置规则如下

- 额外参数只能以字典形式设置
- 字典的一个键值对代表一个参数，键代表参数名，值代表参数值。
- 额外参数需在 name 参数前，否则报 位置参数只能在关键字参数前
- 设置的额外参数只能在视图函数中读取和使用
- 参数值没有数据格式限制，可以为某个对象、字符串或列表（元组）等。

app 路由中设置

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    re_path('dict/(?P<year>[0-9]{4})/', views.myyear_dict, {'month': '05'}, name='myyear_dict', ),  # 设置额外参数（字典）
]
```

views.py 中调用

```python
from django.shortcuts import render, HttpResponse

def myyear_dict(request, year, month):
    return render(request, 'myyear_dict.html', {'month': month})
```

myyear_dict.html 中

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<a href="{% url 'myyear_dict' 2018 %}">2018 {{ month }} Archive</a>
</body>
</html>
```

浏览器访问

![image-20201116160849294](D:\MyDjango\images\image-20201116160849294.png)



# 视图

视图（View）是Django的MTV架构模式的V部分，主要负责处理用户请求和生成相应的响应内容，然后在页面或其他类型文档中显示。也可以理解为视图是MVC架构里面的C部分（控制器），主要处理功能和业务上的逻辑。

# 模板

### 变量与标签

变量是模板中最基本的组成单位，模板变量是由视图函数生成的。如果变量没有被视图函数生成，那么模板引擎解析HTML时，模板变量不会显示在网页上

变量以 `{{ variable }}` 表示，variable 是变量名，变量可以是 Python 支持的数据类型。使用方法如下：

```django
# variable 为字符串或整型
{{ variable }}

# variable 为字典或数据对象，通过点号(.)来访问其属性值
# 如 variable = {'name': 'Lily', 'info': {'home': 'beijing', 'homeplace': 'shanghai'}}
{{ variable.name }}
{{ variable.info.home }}  
```

 模板的标签就如Python里面的函数和方法，Django 常用的内置标签说明如下

| 标签              | 描述                                                |
| :---------------- | --------------------------------------------------- |
| {% for %}         | 遍历输出变量的内容，变量类型应为列表或数组          |
| {% if %}          | 对变量进条件判断                                    |
| {% csrf_token %}  | 生成 csrf_token 的标签，用于防护跨站请求伪造攻击    |
| {% url %}         | 引用路由配置的地址，生成相应的 URL 地址             |
| {% with %}        | 将变量名重新命名                                    |
| {% load %}        | 加载导入 Django 的标签库                            |
| {% static %}      | 读取静态资源的文件内容                              |
| {% extends xxx %} | 模板继承，xxx 为模板文件名，使当前模板继承 xxx 模板 |
| {% block xxx %}   | 重写父类模板的代码                                  |

各标签名用法如下：

```django
# for 循环
{% for item in mylist %}
{{ item }}
{{ endfor }}

# 条件判断
{% if name = 'Lily' %}
{{ name }}
{% elif name = 'Lucy' %}
{{ name }}
{% else %}
{{ name }}
{% endif %}

# 生成不带变量的 URL 地址
# 相关的路由地址：path('', views.index, name='index')
<a href="{% url 'index' %}" target="_blank">首页</a>
# 生成带变量的 URL 地址
# 相关的路由地址：path('search/<int:page>.html', views.index)
<a href="{% url 'index' 1 %}" target="_blank">首页</a>
    
# 变量重命名
{% with total = products_total %}
{{ total }}
{% endwith %}

# load 导入静态文件标签库，staticfiles 来自 settings.py 的 INSTALLED_APPS
{% load staticfiles %}

# static 标签，来自静态文件标签库 staticfiles
{% static "css/hw_index.css" %}
```



for 标签模板变量说明

| 变量               | 描述                                             |
| ------------------ | ------------------------------------------------ |
| forloop.counter    | 获取当前循环的索引，从 1 开始计算                |
| forloop.counter()  | 获取当前循环的索引，从 0 开始计算                |
| forloop.recounter  | 索引从最大数开始递减，知道索引到 1 位置          |
| forloop.recounter  | 索引从最大数开始递减，知道索引到 0 位置索        |
| forloop.first      | 当遍历的元素为第一项时为真                       |
| forloop.last       | 当遍历的元素为最后一项时为真                     |
| forloop.parentloop | 在嵌套的 for 循环中，获取上层 for 循环的 forloop |



orloop 使用方法如下：

```django
{% for name in name_list %}
{% if forloop.counter == 1 %}
	<span>这是第一次循环</span>
{% elif forloop.last %}
	<span>这是最后一次循环</span>
{% else %}
	<span>本次循环次数为：{{ forloop.counter }}</span>
{% endif %}
{% endfor %}
```

### 模板继承

模板继承是通过模板标签来实现的，其作用是将多个HTML模板的共同代码集中在一个新的HTML模板中，然后各个模板可以直接调用新的HTML模板，从而生成HTML网页，这样可以减少模板之间重复的代码

模板继承主要由 `block xxx` 和 `extends xxx` 标签实现

- block xxx ：声明继承的开始位置和结束位置
- extends xxx ：声明继承自哪一个静态 HTML 

共用的基础文件(父类) base.html 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
{% block body %}
{% endblock %}
</body>
</html>
```

继承的文件（子类）

```html
{% extends 'base.html' %}
{% block body %}
<a href="{% url 'temp_inherit' }", target='_blank'>首页</a>
<h1>This a template inherit demo !</h1>
{% endblock %}
```



### 过滤器

过滤器主要是对变量的内容进行处理，如替换、反序和转义等，减少视图函数的代码量

使用方法：``{{ variable | filter }}``

变量支持多个过滤器同时使用：`{{ variable | filter1 | filter2 }}`

有些过滤器还可以传递参数，但仅支持一个参数的传入：`{{ variable | date:"D d M Y"}}`

Django 内置的过滤器

| 内置过滤器       | 使用形式 | 说明 |
| ---------------- | -------- | ---- |
| add              |          |      |
| addslashes       |          |      |
| capfirst         |          |      |
| cut              |          |      |
| date             |          |      |
| default          |          |      |
| default_if_none  |          |      |
| dictsort         |          |      |
| dictsortreversed |          |      |
| 待补充。。。     |          |      |



自定义过滤器

根目录 下创建 `user_defined/templatetags` ，并将 `user_defined` 添加到 `settings.py` 文件中的 `INSTALLED_APPS` 中。

app 下自定义过滤器 只需创建 `templatetags` ，且只需将 app 添加到`settings.py` 文件中的 `INSTALLED_APPS` 中。

注意：`templatetags` 为固定命名，不能修改，否则找不到自定义过滤器

在 `templatetags` 下创建 自定义文件`myfilter`，内容如下

```python
from django import template

# 声明模板对象，也称注册过滤器
register = template.Library()
# 声明并定义过滤器
@register.filter
def myrepalce(value, args):
    oldvalue = args.split(':')[0]
    newvalue = args.split(':')[1]
    return value.replace(oldvalue, newvalue)
```

静态文件中自定义文件 `{% load myfilter %}`，并在变量中使用过滤器 `{{ title | myrepalce:'首页:我的首页' }}`

```html
{% load myfilter %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title | myrepalce:'首页:我的首页' }}</title>
</head>
<body>
<p>this is a user-defined filter demo !</p>
<p>替换前：{{ title }}</p>
<p>替换后：{{ title | myrepalce:'首页:我的首页' }}</p>
</body>
</html>
```

视图函数中传递变量：

```python
def defined_filter(request):
    return render(request, 'index_filter.html', context={'title': '首页'})
```

浏览器访问：

![image-20201117170108853](D:\MyDjango\images\image-20201117170108853.png)



# 模型与数据库

Django对各种数据库提供了很好的支持，包括：PostgreSQL、MySQL、SQLite和Oracle，而且为这些数据库提供了统一的调用API，这些API统称为ORM框架。通过使用Django内置的ORM框架可以实现数据库连接和读写操作

### 构建模型

Django 中利用 ORM 操作数据库的使用方法如下：

- 配置目标数据库信息；配置在 `settings.py` 中的 `DATABASES` 中
- 构建虚拟数据库，在 App 的 model.py 的以类的形式定义模型
- 通过模型在目标数据库中创建响应的数据表
- 在视图函数中通过对模型操作实现目标数据库的读写操作

配置数据库信息：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Django 提供4种数据库引擎
        # 'ENGINE': 'django.db.backends.mysql',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.oracle',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 设置多个数据库，添加多个字典键值对
    'MyDjango': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'django_db',  # 数据库名
        'USER': 'root',  # 用户
        'PASSWORD': '1234',  # 密码
        'HOST': '127.0.0.1',  # 数据库地址
        'PORT': '3306',  # 数据库端口
    },
```



在 App 中 model.py 中定义数据库模型，

- 类表示数据库表，且需继承 `models.Model`
- 属性表示数据库字段

```python
from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
```



在目标数据库创建数据表，项目目录下运行 cmd 命令

> python manage.py makemigrations
>
> python manage.py migrate

其中 `makemigrations `用于创建数据库迁移表，其中包含数据库表的各种信息，`migrate` 则根据数据库迁移表在目标数据库生成对应的数据表

**表字段数据类型及说明**

| 表字段                           | 说明                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| models.AutoField                 | 默认会生成一个名为 id 类型为 int 类型的自增长字段            |
| models.CharField                 | 字符串类型                                                   |
| models.BooleanField              | 布尔类型                                                     |
| models.ComaSeparatedIntegerField | 用逗号分割的整数类型                                         |
| models.DateField                 | 日期（date）类型                                             |
| models.DateTimeField             | 日期（datetime）类型                                         |
| models.Decimal                   | 十进制小数类型                                               |
| models.EmailField                | 字符串类型（正则表达式邮箱）                                 |
| models.FloatField                | 浮点类型                                                     |
| models.IntegerField              | 整数类型                                                     |
| models.BigIntegerField           | 长整数类型                                                   |
| models.IPAddressField            | 字符串类型（IPv4正则表达式）                                 |
| models.GenericIPAddressField     | 字符串类型，参数protocol可以是：both、IPv4和ipv6，验证IP地址 |
| models.NullBooleanField          | 允许为空的布尔类型                                           |
| models.PositiveIntegerField      | 正整数的整数类型                                             |
| models.PositiveSmallIntegerField | 小正整数类型                                                 |
| models.SlugField                 | 包含字母、数字、下划线和连字符的字符串，常用于 URL           |
| models.SmallIntegerField         | 小整数类型，取值范围（-32,768~+32,768）                      |
| models.TextField                 | 长文本类型                                                   |
| models.TimeField                 | 时间类型，显示时分秒 HH:MM[:ss[.uuuuuu]]                     |
| models.URLField                  | 字符串类型，地址为正则表达式                                 |
| models.BinaryField               | 二进制数据类型                                               |

除了字段类型之外，每个表字段还可以设置相应的参数，使得表字段更加完善

字段参数说明如下

| 参数         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| Null         | 如为 True，字段是否可以为空                                  |
| Blank        | 如为 True，设置在 Admin 站点管理中添加数据时可允许空值       |
| Default      | 设置默认值                                                   |
| primary_key  | 如为 True，将字段设置为主键                                  |
| db_column    | 设置数据库中的字段名称                                       |
| Unique       | 如为 True，将字段设置成唯一属性，默认为 False                |
| db_index     | 如为 True，为字段添加数据库索引                              |
| verbose_name | 在 Admin 站点管理设置字段的显示名称                          |
| related_name | 关联对象反向引用描述符，用于多表查询，可解决一个数据表有两个外键同时指向另一个数据表而出现重名的问题 |

