from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Product
from .models import Card
from django.core.paginator import Paginator


# Create your views here.

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})


def newTem(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    card = []
    cardCount = 0
    cardTotal = 0
    if request.user.is_authenticated:
        card = Card.objects.filter(customer=request.user)
        for crd in card:
            cardCount += 1
            cardTotal += crd.amount

    return render(request, 'newTem.html',
                  {'page_obj': page_obj, 'card': card, 'cardCount': cardCount, 'cardTotal': cardTotal})


def details(request, id):
    data = get_object_or_404(Product, id=id)
    print(id)
    return render(request, 'details.html', {"datas": data})



def addToCard(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        user = request.user
        price = product.res
        quantity = 1


        card = Card.objects.filter(customer=request.user)

        if Card.objects.filter(product = product ,customer = user).exists():
            for crd in card:
                if(crd.product == product):
                    quantity = crd.quantity+1
                    Card.objects.filter(product=product, customer=user).update(quantity=quantity,amount=price*quantity)
        else:
            card = Card(product=product, customer=user, quantity=quantity, amount=price * quantity)
            card.save()

        return redirect('/')

    else:
        return redirect('login')



def articles(request):
    keyword = request.GET.get("key")
    if len(keyword) > 0:
        articles = Product.objects.filter(name__contains=keyword)
        if len(articles) > 0:
            return render(request, "articles.html", {"articles": articles})
        else:
            ob = Product()
            ob.name = 'not found'
            ob.img = 'asa.jpg'
            ob.res = 00
            articles = [ob]
            return render(request, "articles.html", {"articles": articles})
    else:
        ob = Product()
        ob.name = 'No Product Found'
        ob.img = 'asa.jpeg'
        ob.res = 000
        articles = [ob]
        return render(request, "articles.html", {"articles": articles})


def pitol(request):
    articles = Product.objects.filter(tag__contains='pitol')
    return render(request, "articles.html", {"articles": articles})


def dinner(request):
    articles = Product.objects.filter(tag__contains='dinner')
    return render(request, "articles.html", {"articles": articles})


def frypan(request):
    articles = Product.objects.filter(tag__contains='frypan')
    return render(request, "articles.html", {"articles": articles})


def steel(request):
    articles = Product.objects.filter(tag__contains='steel')
    return render(request, "articles.html", {"articles": articles})


def rice(request):
    articles = Product.objects.filter(tag__contains='rice')
    return render(request, "articles.html", {"articles": articles})


def pressure(request):
    articles = Product.objects.filter(tag__contains='pressure')
    return render(request, "articles.html", {"articles": articles})


def blender(request):
    articles = Product.objects.filter(tag__contains='blender')
    return render(request, "articles.html", {"articles": articles})


def glass(request):
    articles = Product.objects.filter(tag__contains='glass')
    return render(request, "articles.html", {"articles": articles})


def plastic(request):
    articles = Product.objects.filter(tag__contains='plastic')
    return render(request, "articles.html", {"articles": articles})


def alu(request):
    articles = Product.objects.filter(tag__contains='alu')
    return render(request, "articles.html", {"articles": articles})


def other(request):
    articles = Product.objects.filter(tag__contains='other')
    return render(request, "articles.html", {"articles": articles})
