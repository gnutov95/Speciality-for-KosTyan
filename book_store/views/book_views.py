import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from book_store.models import Book, Author
from book_store.utils import json_decorator, json_returned_book_decorator


# Название переменной	verbose_name (русское название)
# title	"Название"
# author	"Автор"
# year	"Год издания"
# genre	"Жанр"
# price	"Цена"
# stock	"Количество на складе"

@csrf_exempt
@require_http_methods(["POST"])
@json_returned_book_decorator
@json_decorator
def create_book(request) -> JsonResponse:

        data = json.loads(request.body)

        if 'title' not in data:
            return JsonResponse({"Поле Название обязательно!"}, status=400)
        author, created = Author.objects.get_or_create(name = data['author'])

        if Author.objects.filter(name = author.name).exists() and Book.objects.filter(title = data['title']).exists():
            return JsonResponse({"message":"Такая книга уже существует!"}, status=400)
        book = Book(
            title=data['title'],
            author=author,
            year=data.get('year',''),
            genre=data.get('genre',''),
            price=data.get('price',0),
            stock=data.get('stock',0)
        )
        book.save()

        return book


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
@json_returned_book_decorator
@json_decorator
def update_book(request, book_id) -> JsonResponse:
    book = get_object_or_404(Book, id=book_id)
    data = json.loads(request.body)

    if 'title' not in data:
        return JsonResponse({"error": "Поле title обязательно!"}, status=400)

    allowed_fields = ['title', 'year', 'genre', 'price', 'stock']

    for field in allowed_fields:
        if field in data:
            setattr(book, field, data[field])

    book.save()
    return book



@csrf_exempt
@require_http_methods(["GET"])
def list_books(request) -> JsonResponse:
    book = Book.objects.all().order_by('title')
    list_fields = []
    for b in book:
        list_fields.append({
            'id': b.id,
            'title': b.title,
            'author': b.author.name,
            'year': b.year,
            'genre': b.genre,
            'price': float(b.price),
            'stock': b.stock,
        })

    return JsonResponse(list_fields, safe=False)
@csrf_exempt
@require_http_methods(["GET"])
@json_returned_book_decorator
@json_decorator
def get_book(request, book_id) -> JsonResponse:
    book = get_object_or_404(Book, id=book_id)
    return book

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_book(request, book_id) -> JsonResponse:
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return JsonResponse({"status": "success deleted"}, status=200)

