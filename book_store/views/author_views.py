import json

from django.core.handlers import exception
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.backends import django
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from book_store.models import Author
from book_store.utils import json_decorator, json_return_author_decorator


def author_list(request):
    authors = Author.objects.all().values('id', 'name', 'bio', 'birth_date')
    # values() возвращает список словарей, сразу в JSON
    return JsonResponse(list(authors),safe=False)


def get_author(request, author_id) -> JsonResponse:

    author = Author.objects.get(id=author_id)
    books = author.books.all()

    data = {
        'id': author.id,
        'name': author.name,
        'bio': author.bio,
        'birth_date': author.birth_date,
        'books': [
            {
                'id': book.id,
                'title': book.title,
                'year': book.year,
                'genre': book.genre
            } for book in books
        ]
    }

    return JsonResponse(data)

def author_sort(request):
    authors = Author.objects.all().order_by('name').last()
    dict_author = authors.__dict__
    dict_author.pop('_state')
    return JsonResponse(dict_author)


@csrf_exempt
@require_http_methods(["POST"])
@json_return_author_decorator
@json_decorator
def create_authors(request) -> JsonResponse:

        data = json.loads(request.body)

        if not data.get('name'):
            return JsonResponse(
                {'error': 'Поле "name" обязательно'},
                status=400
            )

        author = Author(
            name=data['name'],
            bio=data.get('bio', ''),
            birth_date=data.get('birth_date', None),
        )
        author.save()

        return author



@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@json_return_author_decorator
@json_decorator
def update_authors(request, author_id) -> JsonResponse:

        author = get_object_or_404(Author, id=author_id)
        data = json.loads(request.body)
        if not data.get('name'):
            return JsonResponse({'error': 'Поле name - обязательно'}, status=400)
        fields = ['name', 'bio', 'birth_date']
        for field in fields:
            if field in data:
                setattr(author, field, data[field])
        author.save()


        return author




@csrf_exempt
@require_http_methods(["DELETE"])
@json_decorator
def delete_authors(request, author_id: int) -> JsonResponse:
        author = get_object_or_404(Author, id=author_id)


        # Сохраняем данные для ответа
        author_data = {
            'id': author.id,
            'name': author.name,
            'bio': author.bio,
            'birth_date': author.birth_date,
        }

        # Проверяем наличие книг (если есть связь)
        if hasattr(author, 'book_set') and author.book_set.exists():
            return JsonResponse({
                'error': f'Нельзя удалить автора "{author.name}", так как у него есть книги',
                'books_count': author.book_set.count()
            }, status=400)

        author.delete()

        return JsonResponse({
            'status': 'success',
            'message': f'Автор "{author_data["name"]}" удален',
            'deleted_author': author_data
        }, status=200)



def list_authors(request) -> JsonResponse:

    """
    todo переделать под многие
    :param request:
    :return:
    """
    authors = Author.objects.all().order_by('name')
    authors_list = []
    for author in authors:
        authors_list.append({
            'id': author.id,
            'name': author.name,
            'bio': author.bio,
            'birth_date': author.birth_date,
        })
    return JsonResponse(authors_list,safe=False)

