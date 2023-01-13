from django.shortcuts import render
from rest_framework import viewsets

from .serializers import AuthorRegisterSerializer
from .models import Author


class ProfileRegisterAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer




