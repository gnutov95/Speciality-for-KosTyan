import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from book_store.models import Book, Author
# Название переменной	verbose_name (русское название)
# title	"Название"
# author	"Автор"
# year	"Год издания"
# genre	"Жанр"
# price	"Цена"
# stock	"Количество на складе"

@csrf_exempt
@require_http_methods(["POST"])
def create_book(request):
    try:
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

        return JsonResponse({
            'status': 'success',
            'messega': 'Книга успешно создана!',
            'book': {
                'id': book.id,
                'title': book.title,
                'author': book.author.name,
                'year': book.year,
                'genre': book.genre,
                'price': book.price,
                'stock': book.stock,
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



