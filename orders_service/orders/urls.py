from django.urls import path
from .views import OrderListCreateAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order_list_create'),
]