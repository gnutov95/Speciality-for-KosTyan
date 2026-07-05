import json

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from .models import Author


class AuthorAPITestCase(TestCase):


    def setUp(self):


        self.author1 = Author.objects.create(
            name="Лев Толстой",
            bio="Великий русский писатель",
            birth_date="1828-09-09"
        )
        self.author2 = Author.objects.create(
            name="Федор Достоевский",
            bio="Русский писатель и мыслитель",
            birth_date="1821-11-11"
        )


        self.list_url = reverse('list_authors')
        self.create_url = reverse('create_authors')
        self.detail_url = reverse('get_author', args=[self.author1.id])
        self.update_url = reverse('update_authors', args=[self.author1.id])
        self.delete_url = reverse('delete_authors', args=[self.author1.id])

    def test_list_authors_success(self):

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)  # Должно быть 2 автора

        # Проверяем, что оба автора есть в ответе
        names = [author['name'] for author in data]
        self.assertIn(self.author1.name, names)
        self.assertIn(self.author2.name, names)


    def test_create_author_success(self):

        data = {
            "name": "Антон Чехов",
            "bio": "Русский писатель и драматург",
            "birth_date": "1860-01-29"
        }

        response = self.client.post(
            self.create_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        # Проверяем, что автор создался в БД
        self.assertTrue(Author.objects.filter(name="Антон Чехов").exists())

        # Проверяем ответ
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['author']['name'], "Антон Чехов")

    def test_create_author_missing_name(self):

        data = {
            "bio": "Какой-то писатель",
            "birth_date": "1900-01-01"
        }

        response = self.client.post(
            self.create_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Поле "name" обязательно')

    def test_create_author_invalid_json(self):

        response = self.client.post(
            self.create_url,
            data='{"name": "Толстой" "bio": "Писатель"}',  # Невалидный JSON
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Неверный формат JSON!')

    # ========== ТЕСТЫ ДЛЯ GET (один автор) ==========
    def test_get_author_success(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], self.author1.id)
        self.assertEqual(data['name'], "Лев Толстой")
        self.assertEqual(data['bio'], "Великий русский писатель")

    def test_get_author_not_found(self):

        url = reverse('get_author', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # ========== ТЕСТЫ ДЛЯ UPDATE ==========
    def test_update_author_success(self):

        data = {
            "name": "Лев Николаевич Толстой",
            "bio": "Великий русский писатель и философ"
        }

        response = self.client.put(
            self.update_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Проверяем, что данные обновились в БД
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, "Лев Николаевич Толстой")
        self.assertEqual(self.author1.bio, "Великий русский писатель и философ")

        # Проверяем ответ
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['author']['name'], "Лев Николаевич Толстой")

    def test_update_author_partial(self):

        data = {
            "name": "Л. Н. Толстой"
        }

        response = self.client.patch(
            self.update_url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        # Проверяем, что только имя обновилось
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, "Л. Н. Толстой")
        self.assertEqual(self.author1.bio, "Великий русский писатель")  # Не изменилось

    def test_update_author_not_found(self):

        url = reverse('update_authors', args=[999])
        data = {"name": "Новый автор"}

        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)

    # ========== ТЕСТЫ ДЛЯ DELETE ==========
    def test_delete_author_success(self):

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, 200)

        # Проверяем, что автор удален из БД
        self.assertFalse(Author.objects.filter(id=self.author1.id).exists())

        # Проверяем ответ
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('успешно удален', response_data['message'])

    def test_delete_author_not_found(self):

        url = reverse('delete_authors', args=[999])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)