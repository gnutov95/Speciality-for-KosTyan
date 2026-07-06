from django.urls import path
import book_store.views.author_views as views
from book_store.views import book_views, author_views

urlpatterns = [
    # === READ (список всех авторов) ===
    path('authors/', author_views.list_authors, name='list_authors'),
    path('authors/<int:author_id>/', author_views.get_author, name='get_author'),

    # === CREATE (создать автора) ===
    path('authors/create/', author_views.create_authors, name='create_authors'),
    path('book/create/', book_views.create_book, name='create_book'),

    # === UPDATE (обновить автора) ===
    path('authors/<int:author_id>/update/', author_views.update_authors, name='update_authors'),
    path('book/<int:book_id>/update/', book_views.update_book, name='update_book'),

    # === DELETE (удалить автора) ===
    path('authors/<int:author_id>/delete/', author_views.delete_authors, name='delete_authors'),
]
