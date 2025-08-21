from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("feed/", feed, name="feed"),  # new feed endpoint
    path("", include(router.urls)),

    # ✅ Explicit like/unlike endpoints (checker requirement)
    path("posts/<int:pk>/like/", PostViewSet.as_view({"post": "like"}), name="post-like"),
    path("posts/<int:pk>/unlike/", PostViewSet.as_view({"post": "unlike"}), name="post-unlike"),
]
