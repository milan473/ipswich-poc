from django.test import TestCase
from .models import Book

class BookModelTest(TestCase):
    def setUp(self):
        Book.objects.create(title='Test Book', author='Test Author', price=10.00)

    def test_book_creation(self):
        book = Book.objects.get(title='Test Book')
        self.assertEqual(book.price, 10.00)