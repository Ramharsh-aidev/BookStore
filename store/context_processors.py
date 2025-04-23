# store/context_processors.py
from .models import Book

def cart_context(request):
    """
    Provides cart information (item count and total price) to all templates.
    """
    cart_session = request.session.get('cart', {})
    cart_item_count = 0
    cart_total_price = 0
    cart_books = [] # Store book objects for potential use

    if cart_session:
        book_ids = [int(id) for id in cart_session.keys()]
        books_in_cart = Book.objects.filter(id__in=book_ids)
        books_dict = {str(book.id): book for book in books_in_cart}

        for book_id_str, quantity in cart_session.items():
             book = books_dict.get(book_id_str)
             if book:
                cart_item_count += quantity
                cart_total_price += book.price * quantity
                cart_books.append({'book': book, 'quantity': quantity})
             else:
                 # If book deleted, maybe log this or handle cleanup later
                 pass

    return {
        'cart_item_count': cart_item_count,
        'cart_total_price': cart_total_price,
        # 'cart_books': cart_books # You could pass the full list if needed elsewhere
    }