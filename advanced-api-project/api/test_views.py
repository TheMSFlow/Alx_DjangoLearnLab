from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass")

        # Create test books
        self.book1 = Book.objects.create(title="The Hobbit", author="J.R.R. Tolkien", publication_year=1937)
        self.book2 = Book.objects.create(title="Harry Potter", author="J.K. Rowling", publication_year=1997)
        self.book3 = Book.objects.create(title="Python 101", author="Michael Driscoll", publication_year=2020)

        # API client
        self.client = APIClient()

        # URLs
        self.list_url = reverse('book-list')  # Ensure name in urls.py
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', args=[self.book1.pk])
        self.update_url = reverse('book-update', args=[self.book1.pk])
        self.delete_url = reverse('book-delete', args=[self.book1.pk])

    # -------------------- CRUD TESTS --------------------

    def test_list_books(self):
        """Test retrieving all books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_book_authenticated(self):
        """Test that an authenticated user can create a book."""
        self.client.login(username="testuser", password="pass1234")
        data = {"title": "New Book", "author": "Test Author", "publication_year": 2025}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        """Test that an unauthenticated user cannot create a book."""
        data = {"title": "Unauthorized Book", "author": "No Author", "publication_year": 2025}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Test updating a book as authenticated user."""
        self.client.login(username="testuser", password="pass1234")
        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book_authenticated(self):
        """Test deleting a book as authenticated user."""
        self.client.login(username="testuser", password="pass1234")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # -------------------- FILTER / SEARCH / ORDER --------------------

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(f"{self.list_url}?title=The Hobbit")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "The Hobbit")

    def test_search_books(self):
        """Test searching books by keyword."""
        response = self.client.get(f"{self.list_url}?search=python")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Python 101")

    def test_order_books_by_publication_year_desc(self):
        """Test ordering books by publication year descending."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    # -------------------- PERMISSIONS --------------------

    def test_update_book_unauthenticated(self):
        """Test that an unauthenticated user cannot update."""
        data = {"title": "Blocked Update"}
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthenticated(self):
        """Test that an unauthenticated user cannot delete."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
