from manage_product.models import Product
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets


class ManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    unit_price = serializers.IntegerField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.unit_price = validated_data.get('unit_price', instance.name)
        instance.save()
        return instance


class ProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    res = serializers.IntegerField()
    tag = serializers.CharField(max_length=100)
