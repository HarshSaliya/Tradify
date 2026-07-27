from apps.users.models import Test
from rest_framework import generics
from apps.users.serializers import TestSerializer

# Create your views here.
class TestViewSet(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer