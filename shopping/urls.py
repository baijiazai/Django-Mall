from django.urls import path

from shopping import views

app_name = 'shopping'
urlpatterns = [
    path('index/<book_class>', views.index, name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('get_code', views.get_code, name='get_code'),
]
