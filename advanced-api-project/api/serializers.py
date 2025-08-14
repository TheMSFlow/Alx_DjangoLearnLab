from rest_framework import serializers
from .models import Author, Book

# Serializer for the Book model.
# Converts Book instances to JSON and validates JSON input for creating/updating books.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


# Serializer for the Author model.
# Includes a nested list of books for each author using the related_name 'books'.
class AuthorSerializer(serializers.ModelSerializer):
    # The 'books' field is populated with serialized Book objects (read-only).
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

"""
Relationship Handling in Serializers:
- The Author and Book models have a one-to-many relationship (one Author can have many Books).
- In AuthorSerializer, we define a 'books' field that uses BookSerializer to display all books linked to the Author.
- Because of related_name='books' in the Book model's ForeignKey, we can access an author's books with author.books.all().
- The 'books' field in AuthorSerializer is read-only to prevent adding books directly through the Author endpoint;
  instead, books are created/updated via the BookSerializer.
"""
