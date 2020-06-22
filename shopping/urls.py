from django.urls import path, include

from shopping import views

app_name = 'shopping'
urlpatterns = [
    path('index/<book_class>', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('get_code', views.get_code, name='get_code'),
    path('person', views.PersonView.as_view(), name='person'),
    path('cart/', include([
        path('', views.CartView.as_view(), name='cart'),
        path('add/<int:book_id>', views.add_cart, name='add_cart'),
        path('sub/<int:book_id>', views.sub_cart, name='sub_cart'),
        path('clear', views.clear_cart, name='clear_cart'),
    ]))
]
