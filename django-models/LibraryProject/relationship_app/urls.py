from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Book and library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # ✅ Auth routes using Django's built-in class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # ✅ Registration handled by custom view
    path('register/', views.register_view, name='register'),

     # Role-based views
    path('admin-area/', views.admin_view, name='admin_view'),
    path('librarian-area/', views.librarian_view, name='librarian_view'),
    path('member-area/', views.member_view, name='member_view'),
]
