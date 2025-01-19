from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from events.producer import ProductEventProducer

class ProductListCreateAPIView(APIView):
    """
    Ürün listeleme ve yeni ürün oluşturma API'si.
    """
    def get(self, request):
        # Cache kontrolü
        cache_key = "product_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)  # Cache süresi: 1 saat
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()

            # 'Product Created' olayını yayınla
            producer = ProductEventProducer()
            event = {
                "product_id": product.id,
                "name": product.name,
                "price": float(product.price),
                "stock": product.stock,
            }
            producer.publish_event(event)
            producer.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProductStockAPIView(APIView):
    """
    Ürün stok güncelleme API'si.
    """
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            stock_change = request.data.get("stock_change", 0)
            product.update_stock(stock_change)

            return JsonResponse({"message": "Product stock updated", "product_id": product.id}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product not found"}, status=404)