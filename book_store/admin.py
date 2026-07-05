from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_date')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'year', 'genre')
    list_filter = ('author', 'genre')
    search_fields = ('title',)