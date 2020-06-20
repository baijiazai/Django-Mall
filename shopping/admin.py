from django.contrib import admin

from shopping.models import Book, User


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_class', 'price', 'scale', 'store', 'comments')
    list_filter = ['book_class']
    search_fields = ['name']


class UserAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'username', 'email', 'password')
    search_fields = ['nickname', 'username', 'email']


admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)
