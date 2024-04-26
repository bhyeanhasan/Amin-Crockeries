import io
from manage_product.models import Product
from manage_api.serializers import ProductSerializer, ProductDetailSerializer, ManageUserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ManageUserSerializer


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        profile = Product.objects.all()
        serializer = ProductSerializer(profile, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream_data)
        serializer_complex_data = ProductSerializer(data=python_data)

        if serializer_complex_data.is_valid():
            serializer_complex_data.save()
            res = {'msg': 'Data Created'}
            return JsonResponse(res)

        return JsonResponse(serializer_complex_data.errors)

    if request.method == 'PUT':
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream_data)
        id = python_data.get('id')
        product = Product.objects.get(id=id)
        serializer_complex_data = ProductSerializer(product, data=python_data, partial=True)

        if serializer_complex_data.is_valid():
            serializer_complex_data.save()
            res = {'msg': 'Data Updated'}
            return JsonResponse(res)

        return JsonResponse(serializer_complex_data.errors)

    if request.method == 'DELETE':
        json_data = request.body
        stream_data = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream_data)
        id = python_data.get('id')
        product = Product.objects.get(id=id)
        product.delete()
        res = {'msg': 'Data Deleted'}
        return JsonResponse(res)


@csrf_exempt
def product_details(request, pk):
    if request.method == 'GET':
        profile = Product.objects.get(id=pk)
        serializer = ProductDetailSerializer(profile)
        return JsonResponse(serializer.data, safe=False)
