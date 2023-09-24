from rest_framework import serializers
from manage_product.models import Product


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['name', 'img', 'res', 'tag']


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    res = serializers.IntegerField()
    tag = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.res = validated_data.get('res',instance.name)
        instance.tag = validated_data.get('tag',instance.name)
        instance.save()
        return instance


class ProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    res = serializers.IntegerField()
    tag = serializers.CharField(max_length=100)
