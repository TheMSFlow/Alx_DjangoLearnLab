from django.db import models

# The Author model represents a writer who can have multiple books.
# Each Author object stores the author's name.
class Author(models.Model):
    # name: Stores the full name of the author as text.
    name = models.CharField(max_length=255)

    def __str__(self):
        # This makes the admin and shell display the author's name instead of an object ID.
        return self.name


# The Book model represents a single book written by an Author.
# Each Book is linked to exactly one Author (one-to-many relationship).
class Book(models.Model):
    # title: The title of the book.
    title = models.CharField(max_length=255)
    # publication_year: The year the book was published (integer value).
    publication_year = models.IntegerField()
    # author: Foreign key linking the book to an Author.
    #   - on_delete=models.CASCADE means if an Author is deleted, all their books are deleted too.
    #   - related_name='books' allows reverse lookup: author.books.all()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        # Shows the title and publication year for easy reading in admin and shell.
        return f"{self.title} ({self.publication_year})"
