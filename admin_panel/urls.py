# admin_panel/urls.py
from django.urls import path
from .views import (
    AdminDashboardView, AdminBookListView, AdminBookCreateView,
    AdminBookUpdateView, AdminBookDeleteView
)

app_name = 'admin_panel'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
    path('books/', AdminBookListView.as_view(), name='book_list'),
    path('books/add/', AdminBookCreateView.as_view(), name='book_add'),
    path('books/edit/<int:pk>/', AdminBookUpdateView.as_view(), name='book_edit'),
    path('books/delete/<int:pk>/', AdminBookDeleteView.as_view(), name='book_delete'),
]