from rest_framework import generics, permissions
from django.shortcuts import render

from .serializers import CategorySerializer
from category.models import Category


# Create your views here.


class CategoryCreateListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    # permission_classes = (permissions.IsAdminUser,)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return permissions.IsAdminUser(),
        return permissions.AllowAny(),


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return permissions.AllowAny(),
        return permissions.IsAdminUser(),

