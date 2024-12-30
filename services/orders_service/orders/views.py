from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from events.producer import OrderEventProducer

class OrderListCreateAPIView(APIView):
    """
    Siparişleri listeleme ve yeni sipariş oluşturma API'si.
    """
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            # 'Order Created' olayını yayınla
            producer = OrderEventProducer()
            event = {
                "order_id": order.id,
                "user_id": order.user_id,
                "total_amount": float(order.total_amount),
                "status": order.status,
            }
            producer.publish_event(event)
            producer.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)