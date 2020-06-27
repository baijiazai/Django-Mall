from django.urls import path

from demo import views

app_name = 'demo'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('auth_code', views.auth_code, name='auth_code'),
    path('get_code', views.get_code, name='get_code'),
    path('cache_list', views.cache_list, name='cache_list'),
]