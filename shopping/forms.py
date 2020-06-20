from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from shopping.models import User


class LoginForm(forms.Form):
    # 登录表单
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput)
    check_code = forms.CharField(label='验证码', max_length=6, min_length=6)

    def clean(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
        except User.DoesNotExist:
            user = ''
        # 用户名或密码错误
        if user == '':
            raise ValidationError('用户名或密码错误')
        elif not check_password(self.cleaned_data.get('password'), user.password):
            raise ValidationError('用户名或密码错误')

        return self.cleaned_data


# 注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    email = forms.EmailField(label='邮箱', max_length=254)
    password = forms.CharField(label='密码', max_length=256, min_length=6, widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', max_length=256, min_length=6, widget=forms.PasswordInput)
    check_code = forms.CharField(label='验证码', max_length=6, min_length=6)

    def clean(self):
        # 验证用户名是否存在
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
        except User.DoesNotExist:
            user = ''
        if user:
            raise ValidationError('用户名已存在')
        # 验证邮箱是否存在
        try:
            email = User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            email = ''
        if email:
            raise ValidationError('邮箱已被注册')
        # 验证两次输入的密码是否一致
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('两次输入的密码不一致', code='equal')

        return self.cleaned_data
