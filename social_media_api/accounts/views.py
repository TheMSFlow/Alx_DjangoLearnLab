from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
        }, status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."})

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        if request.user == user_to_unfollow:
            return Response({"detail": "You cannot unfollow yourself."}, status=400)

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You unfollowed {user_to_unfollow.username}."})
