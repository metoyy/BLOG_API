from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        if not represent['parent']:
            represent.pop('parent')
        children = instance.children.all()
        if children:
            represent['children'] = CategorySerializer(children, many=True).data
        return represent
