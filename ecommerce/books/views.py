from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', [])
    cart.append(book.id)
    request.session['cart'] = cart
    return redirect('book_list')

def cart_view(request):
    cart_ids = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart_ids)
    total = sum(book.price for book in books)
    return render(request, 'books/cart.html', {'books': books, 'total': total})