from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from events.producer import UserEventProducer


class RegisterUserAPIView(APIView):
    """
    Yeni kullanıcı kaydı API'si
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Şifreyi hash'leyerek kaydet
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()

            # Kullanıcı oluşturulduğunda event gönder
            producer = UserEventProducer()
            event = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }
            producer.publish_event(event)
            producer.close()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    """
    Kullanıcı giriş API'si
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            return JsonResponse({"message": "Login successful", "user_id": user.id}, status=200)
        return JsonResponse({"message": "Invalid credentials"}, status=401)

class UserProfileAPIView(APIView):
    """
    Kullanıcı profil bilgilerini dönen API.
    Profil bilgileri Redis cache'de saklanır.
    """
    def get(self, request, user_id):
        # Cache'de kullanıcı kontrolü
        cache_key = f"user_profile_{user_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Cache yoksa veritabanından getir ve cache'e ekle
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            cache.set(cache_key, serializer.data, timeout=3600)  # Cache süresi: 1 saat
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)