from django.urls import path

from shopping import views

app_name = 'shopping'
urlpatterns = [
    path('<book_class>', views.index, name='index'),
]
