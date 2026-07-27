from django.urls import path
from apps.users.views import TestViewSet

urlpatterns = [
    path('test/', TestViewSet.as_view(), name="test_view")
]
