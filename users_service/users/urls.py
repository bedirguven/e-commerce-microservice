from django.urls import path
from .views import RegisterUserAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='user_register'),
]