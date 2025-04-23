# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin # For views requiring login
from django.http import Http404

class BookListView(View):
    def get(self, request):
        books = Book.objects.filter(stock__gt=0) # Only show books in stock
        context = {'books': books}
        return render(request, 'store/book_list.html', context)

class BookDetailView(View):
    def get(self, request, pk):
        try:
            book = get_object_or_404(Book, pk=pk)
            context = {'book': book}
            return render(request, 'store/book_detail.html', context)
        except Http404:
             messages.error(request, "Book not found.")
             return redirect('store:book_list')
        except Exception as e:
             messages.error(request, f"An error occurred: {e}")
             return redirect('store:book_list')


class AddToCartView(View):
    # No LoginRequiredMixin here, allow anonymous cart additions
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        quantity = int(request.POST.get('quantity', 1)) # Default to 1 if not specified

        # Get cart from session or create an empty one
        cart = request.session.get('cart', {})
        book_id_str = str(book.id) # Session keys must be strings

        if quantity <= 0:
            messages.warning(request, "Quantity must be positive.")
            return redirect('store:book_detail', pk=pk)

        if book.stock < quantity:
             messages.error(request, f"Not enough stock for '{book.title}'. Available: {book.stock}")
             return redirect('store:book_detail', pk=pk)

        # Update cart
        if book_id_str in cart:
            # Check if adding more exceeds stock
            if book.stock < cart[book_id_str] + quantity:
                 messages.error(request, f"Adding {quantity} exceeds available stock for '{book.title}'. Available: {book.stock}, In Cart: {cart[book_id_str]}")
                 return redirect('store:book_detail', pk=pk)
            cart[book_id_str] += quantity
            messages.success(request, f"Added {quantity} more '{book.title}' to your cart.")
        else:
            cart[book_id_str] = quantity
            messages.success(request, f"Added {quantity} '{book.title}' to your cart.")

        request.session['cart'] = cart
        request.session.modified = True # Important: Mark session as modified

        return redirect('store:cart_view') # Redirect to cart view


class CartView(View):
    def get(self, request):
        cart_session = request.session.get('cart', {})
        cart_items = []
        total_price = 0

        book_ids = [int(id) for id in cart_session.keys()]
        books_in_cart = Book.objects.filter(id__in=book_ids)
        books_dict = {str(book.id): book for book in books_in_cart}

        for book_id_str, quantity in cart_session.items():
            book = books_dict.get(book_id_str)
            if book:
                item_total = book.price * quantity
                cart_items.append({
                    'book': book,
                    'quantity': quantity,
                    'item_total': item_total,
                })
                total_price += item_total
            else:
                # Handle case where book might have been deleted since adding to cart
                # Optionally remove it from session here
                pass

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_empty': not bool(cart_items) # Check if cart is empty after filtering
        }
        return render(request, 'store/cart.html', context)

class RemoveFromCartView(View):
     def post(self, request, pk):
         book_id_str = str(pk)
         cart = request.session.get('cart', {})

         if book_id_str in cart:
             book = get_object_or_404(Book, pk=pk) # Get book details for message
             del cart[book_id_str]
             request.session['cart'] = cart
             request.session.modified = True
             messages.info(request, f"Removed '{book.title}' from your cart.")
         else:
              messages.warning(request, "Item not found in your cart.")

         return redirect('store:cart_view')

class UpdateCartView(View):
    def post(self, request, pk):
        book_id_str = str(pk)
        cart = request.session.get('cart', {})

        if book_id_str not in cart:
            messages.error(request, "Item not found in cart.")
            return redirect('store:cart_view')

        try:
            quantity = int(request.POST.get('quantity'))
            if quantity <= 0:
                 # If quantity is 0 or less, treat as removal
                 del cart[book_id_str]
                 request.session.modified = True
                 messages.info(request, f"Removed item from cart due to zero quantity.")
                 return redirect('store:cart_view')

            book = get_object_or_404(Book, pk=pk)
            if book.stock < quantity:
                messages.error(request, f"Not enough stock for '{book.title}'. Available: {book.stock}")
                return redirect('store:cart_view')

            cart[book_id_str] = quantity
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, f"Updated quantity for '{book.title}'.")

        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity provided.")
        except Book.DoesNotExist:
             messages.error(request, "Book not found.")
             # Optionally remove invalid item from cart
             del cart[book_id_str]
             request.session.modified = True


        return redirect('store:cart_view')