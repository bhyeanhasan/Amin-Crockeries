from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Product, Category
from manage_order.models import Wishlist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


# Create your views here.

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # # for managing card and total calculation
    # card = []
    # cardCount = 0
    # cardTotal = 0
    # if request.user.is_authenticated:
    #     card = Cart.objects.filter(customer=request.user)
    #     for crd in card:
    #         cardCount += 1
    #         cardTotal += crd.amount

    # return render(request, 'newTem.html',{'page_obj': page_obj, 'card': card, 'cardCount': cardCount, 'cardTotal': cardTotal,'category':category})
    categories = Category.objects.all()

    return render(request, 'home.html', {'products': products, 'categories': categories})


def details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'details.html', {"product": product})


def search_result(request):
    keyword = request.GET.get("search")
    products = Product.objects.filter(name__contains=keyword)
    if len(products) > 0:
        return render(request, "listProduct.html", {"products": products})
    else:
        errors = ["Product not Found", "We cannot find any matches for your search term."]
        return render(request, "errorpage.html", {"errors": errors})


def category(request, id):
    products = Product.objects.filter(category__id=id)
    if len(products) > 0:
        return render(request, "listProduct.html", {"products": products})
    else:
        errors = ["Product not Available", "Thanks for your interest", "Stock will available soon"]
        return render(request, 'errorpage.html', {'errors': errors})
