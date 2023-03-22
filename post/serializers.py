from category.serializers import CategorySerializer
from rest_framework import serializers

from comment.serializers import CommentSerializer
from .models import *
from like.serializers import LikeListSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category', 'preview', 'owner_username', 'category_name')

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
        return represent


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['comments_count'] = instance.comments.count()
        represent['comments'] = CommentSerializer(instance=instance.comments.all(), many=True).data
        represent['likes_count'] = instance.likes.count()
        represent['likes'] = LikeListSerializer(instance=instance.likes.all(), many=True).data
        user = self.context['request'].user
        if user.is_authenticated:
            represent['is_liked'] = self.is_liked(instance, user)
        return represent


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    images = PostImageSerializer(many=True, required=False, )

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images',)

    def create(self, validated_data):
        request = self.context['request']
        images_data = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images_data:
            PostImages.objects.create(image=image, post=post)
        return post
