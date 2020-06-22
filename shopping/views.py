import os
import random
from random import randint
import string

from PIL import Image, ImageFont, ImageDraw
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from six import BytesIO

from Mall.settings import STATIC_ROOT
from shopping.forms import LoginForm, RegisterForm
from shopping.models import BOOK_CLASS_LIST, Book, User, Cart


def index(request, book_class):
    book_list = Book.objects.all() if book_class == '全部' else Book.objects.filter(book_class=book_class)
    paginator = Paginator(book_list, 3)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    context = {
        'book_class_list': [b[0] for b in BOOK_CLASS_LIST],
        'book_list': contacts
    }
    return render(request, 'shopping/index.html', context)


# 登录页
class LoginView(View):
    def get(self, request):
        return render(request, 'shopping/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # 验证码验证
            check_code_input = form.cleaned_data.get('check_code')
            check_code = request.session.get('check_code')
            if check_code.lower() != check_code_input.lower():
                form.add_error('check_code', '验证码错误')
            else:
                # 设置 session
                username = form.cleaned_data.get('username')
                user = User.objects.get(username=username)
                request.session['username'] = username
                request.session['user_id'] = user.id
                return redirect(reverse('shopping:index', kwargs={'book_class': '全部'}))
        return render(request, 'shopping/login.html', {'form': form})


# 注册页
class RegisterView(View):
    def get(self, request):
        return render(request, 'shopping/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        # 表单验证通过则创建用户，否则返回页面并给出相应的提示
        if form.is_valid():
            # 验证码验证
            check_code_input = form.cleaned_data.get('check_code')
            check_code = request.session.get('check_code')
            if check_code.lower() != check_code_input.lower():
                form.add_error('check_code', '验证码错误')
            else:
                # 创建用户数据
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                pwd = make_password(password)
                nickname = '无昵称用户'
                icon = ''
                User.objects.create(username=username, email=email, password=pwd, nickname=nickname, icon=icon)
                return redirect(reverse('shopping:login'))
        return render(request, 'shopping/register.html', {'form': form})


# 退出登录
def logout(request):
    # 将 session 恢复默认值
    request.session.flush()
    return redirect(reverse('shopping:index', kwargs={'book_class': '全部'}))


# 验证码
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

    fp = BytesIO()
    img.save(fp, 'png')
    request.session['check_code'] = check_code
    return HttpResponse(fp.getvalue(), content_type='image/png')


# 个人中心
class PersonView(View):
    def get(self, request):
        user_id = request.session.get('user_id', '')
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'shopping/person.html', {'user': user})

    def post(self, request):
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        # 修改头像
        if request.FILES.get('icon'):
            user.icon = request.FILES.get('icon')
            user.save()
        # 修改昵称
        if request.POST.get('nickname'):
            user.nickname = request.POST.get('nickname')
            user.save()
        # 修改密码
        if request.POST.get('oldPassword'):
            if check_password(request.POST.get('oldPassword'), user.password):
                user.password = make_password(request.POST.get('newPassword'))
                user.save()
            else:
                return render(request, 'shopping/person.html', {'error': '原始密码错误！', 'user': user})
        return redirect(reverse('shopping:person', kwargs={'pk': user_id}))


# 购物车列表
class CartView(View):
    def get(self, request):
        user_id = request.session.get('user_id', '')
        cart_list = Cart.objects.filter(user_id=user_id)
        return render(request, 'shopping/cart.html', {'cart_list': cart_list})

    def post(self, request):
        pass


# 加入购物车或数量加一
def add_cart(request, book_id):
    user_id = request.session.get('user_id', '')
    data = {
        'status': 200,
        'msg': 'add success',
    }
    try:
        cart = Cart.objects.get(user_id=user_id, book_id=book_id)
        cart.count = cart.count + 1
        cart.save()
        data['count'] = cart.count
    except:
        Cart.objects.create(user_id=user_id, book_id=book_id)
        data['count'] = 1
    return JsonResponse(data=data)


# 移出购物车或数量减一
def sub_cart(request, book_id):
    user_id = request.session.get('user_id', '')
    try:
        cart = Cart.objects.get(user_id=user_id, book_id=book_id)
        data = {
            'status': 200,
            'msg': 'sub success',
        }
        if cart.count == 1:
            cart.delete()
            data['count'] = 0
        else:
            cart.count = cart.count - 1
            cart.save()
            data['count'] = cart.count
    except:
        data = {
            'status': 404,
            'msg': 'is not exits'
        }
    return JsonResponse(data=data)


# 清空购物车
def clear_cart(request):
    user_id = request.session.get('user_id')
    Cart.objects.filter(user_id=user_id).delete()
    return redirect(reverse('shopping:cart'))
