import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return []

# 2. List all books in a library
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []

# 3. Retrieve the librarian for a library (explicit query)
def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ direct get using FK
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Example usage
if __name__ == "__main__":
    print("\nBooks by 'Jane Austen':")
    for book in books_by_author("Jane Austen"):
        print(f"- {book.title}")

    print("\nBooks in 'Central Library':")
    for book in books_in_library("Central Library"):
        print(f"- {book.title} by {book.author.name}")

    print("\nLibrarian for 'Central Library':")
    librarian = librarian_for_library("Central Library")
    if librarian:
        print(f"- {librarian.name}")
    else:
        print("- No librarian assigned")
