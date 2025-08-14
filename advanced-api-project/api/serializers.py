from rest_framework import serializers
from .models import Author, Book

# Serializer for the Book model.
# This converts Book model instances into JSON and validates incoming JSON data
# before creating or updating Book objects in the database.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Custom validation for the 'publication_year' field.

        - Ensures the publication year is within a realistic range.
        - Uses serializers.ValidationError to raise a user-friendly error message
          if the value is invalid.
        - This method will automatically be called by Django REST Framework
          whenever the 'publication_year' field is present in incoming data.

        Args:
            value (int): The year provided in the API request.

        Returns:
            int: The validated year value if it passes the check.

        Raises:
            serializers.ValidationError: If the year is outside the range 1450–2100.
        """
        if value < 1450 or value > 2100:
            raise serializers.ValidationError(
                "Publication year must be between 1450 and 2100."
            )
        return value


# Serializer for the Author model.
# Includes a nested representation of related Book objects via the 'books' field.
# This allows clients to see all books written by an author when retrieving author details.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to display related Book objects.
    # 'read_only=True' means books cannot be added directly through the Author endpoint.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    def validate_name(self, value):
        """
        Custom validation for the 'name' field.

        - Ensures the author's name is not empty or too short.
        - Uses serializers.ValidationError to return a 400 Bad Request
          with a clear error message if the input is invalid.

        Args:
            value (str): The author name provided in the request.

        Returns:
            str: The validated name if it passes the check.

        Raises:
            serializers.ValidationError: If the name is shorter than 2 characters
              or contains only whitespace.
        """
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Author name must have at least 2 characters."
            )
        return value


"""
Relationship Handling in Serializers:
--------------------------------------
- The Author and Book models have a one-to-many relationship
  (one Author can have multiple Books).
- The 'author' ForeignKey in the Book model uses related_name='books', allowing
  reverse lookups: author.books.all()
- In AuthorSerializer, we use the nested BookSerializer with many=True
  to serialize all related books for an author.
- Nested serialization here is read-only, meaning books are created/updated
  through the BookSerializer directly, not via the Author endpoint.
- Validation methods in both serializers leverage serializers.ValidationError
  to enforce data integrity rules before saving to the database.
"""
