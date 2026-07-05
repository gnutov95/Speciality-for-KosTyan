

from django.contrib import admin
from django.urls import path
import book_store.views as views

urlpatterns = [
    # === READ (список всех авторов) ===
    path('authors/', views.list_authors, name='list_authors'),
    path('authors/<int:author_id>/', views.get_author, name='get_author'),

    # === CREATE (создать автора) ===
    path('authors/create/', views.create_authors, name='create_authors'),

    # === UPDATE (обновить автора) ===
    path('authors/<int:author_id>/update/', views.update_authors, name='update_authors'),

    # === DELETE (удалить автора) ===
    path('authors/<int:author_id>/delete/', views.delete_authors, name='delete_authors'),
]
