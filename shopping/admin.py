from django.contrib import admin

from shopping.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_class', 'price', 'scale', 'store', 'comments')
    list_filter = ['book_class']
    search_fields = ['name']


admin.site.register(Book, BookAdmin)
