# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy # For success URLs

from store.models import Book
from .mixins import StaffRequiredMixin # Import the custom mixin

# Note: Using StaffRequiredMixin automatically handles login check as well

class AdminDashboardView(StaffRequiredMixin, View):
    def get(self, request):
        # Can add more stats later (e.g., total books, users)
        book_count = Book.objects.count()
        context = {'book_count': book_count}
        return render(request, 'admin_panel/dashboard.html', context)

class AdminBookListView(StaffRequiredMixin, View):
    def get(self, request):
        books = Book.objects.all().order_by('-created_at') # Show all books
        context = {'books': books}
        return render(request, 'admin_panel/book_list.html', context)

class AdminBookCreateView(StaffRequiredMixin, View):
    def get(self, request):
        # Pass an empty context for the form template
        return render(request, 'admin_panel/book_form.html', {'action': 'Create'})

    def post(self, request):
        # Manual form processing
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description', '') # Optional
        price_str = request.POST.get('price')
        stock_str = request.POST.get('stock')

        # Manual Validation
        errors = {}
        if not title: errors['title'] = "Title is required."
        if not author: errors['author'] = "Author is required."
        if not price_str: errors['price'] = "Price is required."
        if not stock_str: errors['stock'] = "Stock is required."

        price = None
        if price_str:
            try:
                price = float(price_str)
                if price < 0: errors['price'] = "Price cannot be negative."
            except ValueError:
                errors['price'] = "Invalid price format."

        stock = None
        if stock_str:
            try:
                stock = int(stock_str)
                if stock < 0: errors['stock'] = "Stock cannot be negative."
            except ValueError:
                errors['stock'] = "Invalid stock format (must be an integer)."

        if errors:
            messages.error(request, "Please correct the errors below.")
            context = {
                'action': 'Create',
                'errors': errors,
                'book': request.POST # Pass back the POST data to repopulate form
            }
            return render(request, 'admin_panel/book_form.html', context)

        # Create Book if valid
        try:
            Book.objects.create(
                title=title,
                author=author,
                description=description,
                price=price,
                stock=stock
            )
            messages.success(request, f"Book '{title}' created successfully.")
            return redirect('admin_panel:book_list')
        except Exception as e:
             messages.error(request, f"An error occurred while creating the book: {e}")
             context = {'action': 'Create', 'book': request.POST } # Repopulate form
             return render(request, 'admin_panel/book_form.html', context)


class AdminBookUpdateView(StaffRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        context = {'book': book, 'action': 'Update'}
        return render(request, 'admin_panel/book_form.html', context)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        # Manual form processing
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description', '')
        price_str = request.POST.get('price')
        stock_str = request.POST.get('stock')

        # Manual Validation (similar to create view)
        errors = {}
        if not title: errors['title'] = "Title is required."
        if not author: errors['author'] = "Author is required."
        if not price_str: errors['price'] = "Price is required."
        if not stock_str: errors['stock'] = "Stock is required."

        price = None
        if price_str:
            try:
                price = float(price_str)
                if price < 0: errors['price'] = "Price cannot be negative."
            except ValueError:
                errors['price'] = "Invalid price format."

        stock = None
        if stock_str:
            try:
                stock = int(stock_str)
                if stock < 0: errors['stock'] = "Stock cannot be negative."
            except ValueError:
                errors['stock'] = "Invalid stock format (must be an integer)."

        if errors:
            messages.error(request, "Please correct the errors below.")
            context = {
                'action': 'Update',
                'errors': errors,
                'book': book # Pass original book data mixed with POST data for repopulation
            }
            # Update context with POST values to show attempted changes
            context['book'].title = title
            context['book'].author = author
            context['book'].description = description
            context['book'].price = price_str # Show raw input on error
            context['book'].stock = stock_str # Show raw input on error
            return render(request, 'admin_panel/book_form.html', context)

        # Update Book if valid
        try:
            book.title = title
            book.author = author
            book.description = description
            book.price = price
            book.stock = stock
            book.save()
            messages.success(request, f"Book '{book.title}' updated successfully.")
            return redirect('admin_panel:book_list')
        except Exception as e:
             messages.error(request, f"An error occurred while updating the book: {e}")
             context = {'action': 'Update', 'book': book} # Pass original book back
             # Repopulate with attempted changes
             context['book'].title = title
             context['book'].author = author
             context['book'].description = description
             context['book'].price = price_str
             context['book'].stock = stock_str
             return render(request, 'admin_panel/book_form.html', context)


class AdminBookDeleteView(StaffRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        context = {'book': book}
        return render(request, 'admin_panel/book_confirm_delete.html', context)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        try:
            title = book.title # Get title before deleting
            book.delete()
            messages.success(request, f"Book '{title}' deleted successfully.")
            return redirect('admin_panel:book_list')
        except Exception as e:
             messages.error(request, f"An error occurred while deleting the book: {e}")
             # Redirect back to list or confirmation page on error
             return redirect('admin_panel:book_list')