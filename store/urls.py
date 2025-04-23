# store/urls.py
from django.urls import path
from .views import (
    BookListView, BookDetailView, AddToCartView, CartView,
    RemoveFromCartView, UpdateCartView
)

app_name = 'store'

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart_view'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/<int:pk>/', UpdateCartView.as_view(), name='update_cart'), # Add this URL
]