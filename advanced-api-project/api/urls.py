from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # GET: List all books
    path('books/', BookListView.as_view(), name='book-list'),

    # GET: Retrieve a single book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # POST: Create a book
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # PUT/PATCH: Update a book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),

    # DELETE: Delete a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
