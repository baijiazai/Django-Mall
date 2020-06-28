import os
import random
from random import randint
import string

from PIL import Image, ImageFont, ImageDraw
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from six import BytesIO

from Mall.settings import STATIC_ROOT
from shopping.forms import LoginForm, RegisterForm
from shopping.models import BOOK_CLASS_LIST, Book, User, Cart, Order, OrderBook, Collect, Comment


def index(request, book_class):
    book_list = Book.objects.all() if book_class == '全部' else Book.objects.filter(book_class=book_class)
    collect_list = Collect.objects.filter(user_id=request.session.get('user_id', 0))
    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    context = {
        'book_class_list': [b[0] for b in BOOK_CLASS_LIST],
        'book_list': contacts,
        'collect_list': collect_list
    }
    return render(request, 'shopping/index.html', context)


# 搜索
def search(request):
    keyword = request.GET.get('keyword')
    book_list = Book.objects.filter(name__icontains=keyword).order_by('-scale')
    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    context = {
        'book_list': contacts,
        'keyword': keyword
    }
    return render(request, 'shopping/search.html', context)


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
        user_id = request.session.get('user_id', 0)
        user = get_object_or_404(User, pk=user_id)
        order_list = Order.objects.filter(user_id=user_id)
        pay_order_list = Order.objects.filter(user_id=user_id, status='待付款')
        send_order_list = Order.objects.filter(user_id=user_id, status='待发货')
        take_order_list = Order.objects.filter(user_id=user_id, status='待收货')
        eval_order_list = Order.objects.filter(user_id=user_id, status='待评价')
        collect_list = Collect.objects.filter(user_id=user_id)
        context = {
            'user': user,
            'order_list': order_list,
            'pay_order_list': pay_order_list,
            'send_order_list': send_order_list,
            'take_order_list': take_order_list,
            'eval_order_list': eval_order_list,
            'collect_list': collect_list
        }
        return render(request, 'shopping/person.html', context)

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
        return redirect(reverse('shopping:person'))


# 购物车列表
class CartView(View):
    def get(self, request):
        user_id = request.session.get('user_id', 0)
        cart_list = Cart.objects.filter(user_id=user_id)
        return render(request, 'shopping/cart.html', {'cart_list': cart_list})

    def post(self, request):
        user_id = request.session.get('user_id', 0)
        cbx = request.POST.getlist('sel')
        cart_list = Cart.objects.filter(user_id=user_id, book_id__in=cbx)

        total = round(sum([c.count * c.book.price for c in cart_list]), 2)
        order = Order.objects.create(user_id=user_id, total=total, time=timezone.now(), status='待付款')
        for c in cart_list:
            OrderBook.objects.create(order_id=order.id, book_id=c.book.id, count=c.count)
            c.delete()
        return redirect(reverse('shopping:order_detail', kwargs={'order_id': order.id}))


# 加入购物车或数量加一
def add_cart(request, book_id):
    user_id = request.session.get('user_id', 0)
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
    user_id = request.session.get('user_id', 0)
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


# 订单详情
def order_detail(request, order_id):
    user_id = request.session.get('user_id')
    order = get_object_or_404(Order, pk=order_id, user_id=user_id)
    return render(request, 'shopping/order_detail.html', {'order': order})


# 待付款，付款
def order_pay(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(user_id=user_id, pk=order_id, status='待付款')
            order.status = '待发货'
            order.save()
        except:
            return render(request, 'shopping/order_detail.html', {'msg': '订单不存在'})
        return redirect(reverse('shopping:person'))


# 待收货，收货
def order_take(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(user_id=user_id, pk=order_id, status='待收货')
            order.status = '待评价'
            order.save()
        except:
            return render(request, 'shopping/order_detail.html', {'msg': '订单不存在'})
        return redirect(reverse('shopping:person'))


# 待评价，评价
def order_eval(request):
    return None


# 添加或删除收藏
def edit_collect(request, op, book_id):
    user_id = request.session.get('user_id', 0)
    if op == 'add':
        Collect.objects.create(user_id=user_id, book_id=book_id)
    elif op == 'sub':
        collect = get_object_or_404(Collect, user_id=user_id, book_id=book_id)
        collect.delete()
    return redirect(reverse('shopping:book_detail', kwargs={'book_id': book_id}))


# 书籍详情
def book_detail(request, book_id):
    user_id = request.session.get('user_id', 0)
    book = get_object_or_404(Book, pk=book_id)
    is_collect = Collect.objects.filter(user_id=user_id, book_id=book_id)
    comment_list = Comment.objects.filter(book_id=book_id)
    context = {
        'book': book,
        'is_collect': is_collect,
        'comment_list': comment_list
    }
    return render(request, 'shopping/book_detail.html', context)


# 评论
def add_comment(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', 0)
        book_id = request.POST.get('book_id')
        content = request.POST.get('content')
        book = get_object_or_404(Book, pk=book_id)
        Comment.objects.create(book_id=book_id, user_id=user_id, content=content)
        book.comments = book.comments + 1
        book.save()
        return redirect(reverse('shopping:book_detail', kwargs={'book_id': book.id}))


# 删除评论
def sub_comment(request, comment_id):
    user_id = request.session.get('user_id', 0)
    comment = get_object_or_404(Comment, user_id=user_id, pk=comment_id)
    book_id = comment.book_id
    book = get_object_or_404(Book, pk=book_id)
    comment.delete()
    book.comments = book.comments - 1
    book.save()
    return redirect(reverse('shopping:book_detail', kwargs={'book_id': book.id}))

