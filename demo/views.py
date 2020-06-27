import os
import random
import time
from random import randint
import string

from PIL import Image, ImageFont, ImageDraw
from django.core.cache import caches
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.six import BytesIO
from django.views.decorators.cache import cache_page

from Mall.settings import STATIC_ROOT
from demo.models import Upload


def index(request):
    return HttpResponse('hello demo')


# 上传图片
def upload(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        Upload.objects.create(img=img)
        return HttpResponseRedirect(reverse('demo:upload'))
    images = Upload.objects.all()
    return render(request, 'demo/upload.html', {'images': images})


# 验证码
def auth_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        msg = '对' if input_code == request.session.get('check_code') else '错'
        return render(request, 'demo/auth_code.html', {'msg': msg})
    return render(request, 'demo/auth_code.html')


# 获取验证码
def get_code(request):
    img = Image.new('RGB', (120, 60), (255, 255, 255))
    font = ImageFont.truetype(os.path.join(STATIC_ROOT, 'demo/fonts/DroidSans.ttf'), randint(25, 30))
    draw = ImageDraw.Draw(img)
    check_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    # 元素点
    for _ in range(1000):
        draw.point((randint(0, 120), randint(0, 60)), (randint(0, 255), randint(0, 255), randint(0, 255)))
    # 验证码
    for i in range(6):
        draw.text((5 + i * 20, randint(5, 35)), check_code[i], (0, 0, 0), font)
    # 横线
    for x in range(0, 121):
        for y in range(15, 46, 15):
            draw.point((x, y), (0, 0, 0))
    # 缓存
    fp = BytesIO()
    img.save(fp, 'png')
    request.session['check_code'] = check_code
    return HttpResponse(fp.getvalue(), content_type='image/png')


def cookie_demo(request):
    response = HttpResponse('Hello World!')
    # 设置 cookie (key, value, max_age=最大过期时间，单位秒/s)
    response.set_cookie('user', 'lala', max_age=60)
    # 获取 cookie
    request.COOKIES.get('user')
    # 设置加盐 cookie (key, value, salt=加盐字符串)
    response.set_signed_cookie('name', 'lala', salt='haha')
    # 获取加盐 cookie (key, salt=加盐字符串)
    request.get_signed_cookie('name', salt='haha')
    # 删除单个 cookie
    response.delete_cookie('user')
    return response


def session_demo(request):
    # 设置 session
    request['user'] = 'lala'
    # 获取 session
    request.session.get('user')
    # 删除当前 session 并删除 cookie
    request.session.flush()
    # 清空 session
    request.session.clear()


# 数据库缓存
@cache_page(timeout=60, cache='default')
def cache_list(request):
    arr = ['The number is %d' % i for i in range(10)]
    time.sleep(5)  # 伪装耗时
    return render(request, 'demo/cache_list.html', {'arr': arr})


# 内存缓存
@cache_page(timeout=60, cache='redis_backend')
def redis_cache_list(request):
    arr = ['The number is %d' % i for i in range(10)]
    time.sleep(5)  # 伪装耗时
    return render(request, 'demo/cache_list.html', {'arr': arr})
