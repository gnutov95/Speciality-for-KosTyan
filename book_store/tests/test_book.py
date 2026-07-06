from django.test import TestCase
from django.urls import reverse

from book_store.models import Book


class BookAPITestCase(TestCase):
    def setUp(self):
        self.book1 = Book.objects.create(

            title = "Идиот",
            author= "Федор Достоевский",
            year = 1932,
            genre= "Литература",
            price =float(231),
            stock = 12,

        )
        self.book2 = Book.objects.create(

            title="ЦПС",
            author="Костя Горбачев",
            year=2026,
            genre="Отчет",
            price=float(12),
            stock=3,

        )


        self.list_url = reverse('list_books')
        self.create_url = reverse('create_book')
        self.detail_url = reverse('get_book', args=[self.book1.id])
        self.update_url = reverse('update_book', args=[self.book1.id])
        self.delete_url = reverse('delete_book', args=[self.book1.id])


