from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from . import serializers
from .permissions import *


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        # only admin or author can delete
        if self.action == 'destroy':
            return permissions.IsAuthenticated(), IsAuthorOrAdmin(),
        # only author can update
        elif self.action in ('update', 'partial_update'):
            return permissions.IsAuthenticated(), IsAuthor(),
        # listing and retrieve is allowAny, but create is for authorized only
        return permissions.IsAuthenticatedOrReadOnly(),


'''class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializer
        return serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdmin(),
        elif self.request.method in ('PUT', 'PATCH'):
            return IsAuthor(),
        return permissions.AllowAny(),
'''

