from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CustomAuthToken, ProfileView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),  # this brings in /users/, /users/{id}/follow/, etc.
]
