from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.users.models import User
from apps.users.serializers import RegisterSerializers


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
    permission_classes = [AllowAny]
