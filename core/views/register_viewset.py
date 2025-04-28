from django.contrib.auth.models import User
from rest_framework import generics
from core.serializers.register_serializer import RegisterSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer