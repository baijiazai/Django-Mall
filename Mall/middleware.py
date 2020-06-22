from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from shopping.models import User

NEED_LOGIN = [
    reverse('shopping:person'),
    reverse('shopping:cart'),
]


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in NEED_LOGIN:
            user_id = request.session.get('user_id', '')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    request.user = user
                except:
                    return redirect(reverse('shopping:login'))
            else:
                return redirect(reverse('shopping:login'))
