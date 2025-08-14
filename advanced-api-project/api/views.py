from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    GET /api/books/
    ----------------
    - Retrieves a list of all Book instances.
    - Publicly accessible (no authentication required).
    - Uses DRF's ListAPIView to automatically handle:
        * Querying all objects
        * Serializing them to JSON
        * Applying pagination/filters if enabled in settings.py
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can access


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<int:pk>/
    ------------------------
    - Retrieves a single Book instance by its primary key (ID).
    - Publicly accessible (no authentication required).
    - Returns HTTP 404 if no matching book is found.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/
    -----------------------
    - Creates a new Book instance.
    - Requires authentication (IsAuthenticated).
    - Uses BookSerializer to validate and save incoming JSON data.
    - Includes custom validation in `create()` method to:
        * Prevent publication years beyond 2100.
    - Adds a custom success message in the API response.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Extra validation beyond serializer rules
        if 'publication_year' in request.data and int(request.data['publication_year']) > 2100:
            return Response(
                {"error": "Publication year cannot be in the far future."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Book created successfully!"
        return response


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /api/books/<int:pk>/update/
    PATCH /api/books/<int:pk>/update/
    --------------------------------
    - Updates an existing Book instance.
    - Requires authentication (IsAuthenticated).
    - Accepts both full updates (PUT) and partial updates (PATCH).
    - Includes custom validation in `update()` method to:
        * Prevent titles shorter than 2 characters.
    - Adds a custom success message in the API response.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Additional field-level validation
        if 'title' in request.data and len(request.data['title']) < 2:
            return Response(
                {"error": "Title must be at least 2 characters long."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Book updated successfully!"
        return response


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<int:pk>/delete/
    ----------------------------------
    - Deletes a Book instance by its primary key (ID).
    - Requires authentication (IsAuthenticated).
    - Returns HTTP 204 No Content on success.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
