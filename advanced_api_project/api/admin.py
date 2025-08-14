from django.contrib import admin
from .models import Author, Book

# Register models so they appear in the admin panel
admin.site.register(Author)
admin.site.register(Book)
