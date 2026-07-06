import json

from django.http import JsonResponse

from book_store.models import Book


def json_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse(
                {'error': 'Неверный формат JSON!'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'error': str(e)},
                status=400
            )
    return wrapper

def json_returned_book_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            book = func(*args, **kwargs)
            if isinstance(book, JsonResponse):
                return book
            return JsonResponse({
                'status': 'success',
                'book': {
                    'id': book.id,
                    'title': book.title,
                    'author': book.author.name,
                    'year': book.year,
                    'genre': book.genre,
                    'price': float(book.price),
                    'stock': book.stock,
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return wrapper

def json_return_author_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            author = func(*args, **kwargs)

            if isinstance(author, JsonResponse):
                return author
            return JsonResponse({
                'status': 'success',
                'message': f'Автор "{author.name}" успешно обновлен!',
                'author': {
                    'id': author.id,
                    'name': author.name,
                    'bio': author.bio,
                    'birth_date': author.birth_date,
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return wrapper