from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# ✅ Function-based view that uses the correct template path and query
def list_books(request):
    books = Book.objects.all()  # ✅ Required line
    return render(request, 'relationship_app/templates/list_books.html', {'books': books})  # ✅ Required path

# ✅ Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/templates/library_detail.html'  # Match template location
    context_object_name = 'library'
