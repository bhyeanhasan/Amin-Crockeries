from mainapp.models import Product
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import ProductSerializer,CustomSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        profile = Product.objects.all()
        serializer = ProductSerializer(profile, many=True)
        return JsonResponse(serializer.data, safe=False)
@csrf_exempt
def custom_serializer(request):
    if request.method == 'GET':
        profile = Product.objects.all()
        serializer = CustomSerializer(profile, many=True)
        return JsonResponse(serializer.data, safe=False)