# API View Configurations – Advanced API Project

This document describes the Django REST Framework views for managing `Book` instances.

---

## Views Overview

### 1. **BookListView**
- **URL**: `/api/books/`
- **Method**: `GET`
- **Description**: Returns a list of all books.
- **Access**: Public (no authentication required).
- **Base Class**: `ListAPIView`.

---

### 2. **BookDetailView**
- **URL**: `/api/books/<int:pk>/`
- **Method**: `GET`
- **Description**: Retrieves details of a single book by ID.
- **Access**: Public.
- **Base Class**: `RetrieveAPIView`.

---

### 3. **BookCreateView**
- **URL**: `/api/books/create/`
- **Method**: `POST`
- **Description**: Creates a new book.
- **Access**: Authenticated users only.
- **Base Class**: `CreateAPIView`.
- **Custom Behavior**:
  - Validates that `publication_year` is ≤ 2100.
  - Adds a `"message"` field in the success response.

---

### 4. **BookUpdateView**
- **URL**: `/api/books/<int:pk>/update/`
- **Methods**: `PUT`, `PATCH`
- **Description**: Updates an existing book.
- **Access**: Authenticated users only.
- **Base Class**: `UpdateAPIView`.
- **Custom Behavior**:
  - Ensures `title` has at least 2 characters.
  - Adds a `"message"` field in the success response.

---

### 5. **BookDeleteView**
- **URL**: `/api/books/<int:pk>/delete/`
- **Method**: `DELETE`
- **Description**: Deletes a book.
- **Access**: Authenticated users only.
- **Base Class**: `DestroyAPIView`.

---

## Permissions Summary
| View            | Permission Class          | Access            |
|-----------------|---------------------------|-------------------|
| BookListView    | `AllowAny`                 | Public            |
| BookDetailView  | `AllowAny`                 | Public            |
| BookCreateView  | `IsAuthenticated`          | Authenticated     |
| BookUpdateView  | `IsAuthenticated`          | Authenticated     |
| BookDeleteView  | `IsAuthenticated`          | Authenticated     |

---

## Hooks and Customizations
- **`create()` method override** in `BookCreateView`:
  - Adds custom validation for `publication_year`.
  - Appends a success message to the response.
- **`update()` method override** in `BookUpdateView`:
  - Adds custom validation for `title` length.
  - Appends a success message to the response.
- **Permissions**:
  - Public read access (`AllowAny`) for listing and viewing books.
  - Restricted write access (`IsAuthenticated`) for create, update, and delete.

---

## Example Request/Response

**POST** `/api/books/create/`  
```json
{
  "title": "The Pragmatic Programmer",
  "publication_year": 1999,
  "author": 1
}

## Filtering, Searching, and Ordering

**Base URL:** `/api/books/`

### Filtering
- `?title=Book Title`
- `?author__name=Author Name`
- `?publication_year=YYYY`

### Searching
- `?search=keyword` (searches in title and author name)

### Ordering
- `?ordering=title` (A → Z)
- `?ordering=-title` (Z → A)
- `?ordering=publication_year` (oldest → newest)
- `?ordering=-publication_year` (newest → oldest)


## Running Tests

1. Run all tests:
```bash
python manage.py test api
