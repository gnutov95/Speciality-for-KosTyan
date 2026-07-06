import json

from django.http import JsonResponse


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