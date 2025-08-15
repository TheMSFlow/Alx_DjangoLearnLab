from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),

    path("login/", auth_views.LoginView.as_view(
        template_name="blog/login.html"
    ), name="login"),

    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),

    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    # Comments
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Search
    path('search/', views.post_search, name='post-search'),

    #Tags
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts-by-tag'),


]
