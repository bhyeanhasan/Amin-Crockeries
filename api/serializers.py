from rest_framework import serializers
from mainapp.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'img', 'res', 'tag']


class CustomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    res = serializers.IntegerField()
    tag = serializers.CharField(max_length=100)
