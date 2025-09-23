from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Book, Order


# ==============================
#   Book Browsing (List & Detail)
# ==============================

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Get cart from session
    cart = request.session.get('cart', {})

    # 🔑 Fix: if cart is a list, reset it to dict
    if isinstance(cart, list):
        cart = {}

    # Always use string key
    book_id_str = str(book.id)
    cart[book_id_str] = cart.get(book_id_str, 0) + 1

    # Save back to session
    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f"Added {book.title} to cart!")
    return redirect('book_list')


def cart_view(request):
    # Get cart from session (dictionary: book_id -> quantity)
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for book_id, quantity in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            line_total = book.price * quantity
            total += line_total
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'line_total': line_total
            })
        except Book.DoesNotExist:
            pass  # skip if book doesn't exist

    return render(request, 'books/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # Simulate order (no user auth for now)
        messages.success(request, f"Successfully purchased {book.title}!")
        # Clear cart item for this book
        cart = request.session.get('cart', {})
        if book.id in cart:
            del cart[book.id]
            request.session['cart'] = cart
        return redirect('purchase_success')
    return render(request, 'books/buy_confirmation.html', {'book': book})

def purchase_success(request):
    return render(request, 'books/purchase_success.html')