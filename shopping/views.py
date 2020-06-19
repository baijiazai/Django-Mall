from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from shopping.models import BOOK_CLASS_LIST, Book


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