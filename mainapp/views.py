from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .models import Product
from .models import Card
from .models import Wishlist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


# Create your views here.



def product_list(request):
    category = (
        ('pitol', 'Pitol'),
        ('dinner', 'Dinner Set'),
        ('plastic', 'Plastic'),
        ('cooker', 'Cooker'),
    )

    # for rendering all products
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # for managing card and total calculation
    card = []
    cardCount = 0
    cardTotal = 0
    if request.user.is_authenticated:
        card = Card.objects.filter(customer=request.user)
        for crd in card:
            cardCount += 1
            cardTotal += crd.amount


    return render(request, 'newTem.html',{'page_obj': page_obj, 'card': card, 'cardCount': cardCount, 'cardTotal': cardTotal,'category':category})


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

        if Card.objects.filter(product=product, customer=user).exists():
            for crd in card:
                if (crd.product == product):
                    quantity = crd.quantity + 1
                    Card.objects.filter(product=product, customer=user).update(quantity=quantity,
                                                                               amount=price * quantity)
        else:
            card = Card(product=product, customer=user, quantity=quantity, amount=price * quantity)
            card.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect('login')


def deletefromcart(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        user = request.user
        price = product.res
        quantity = 0

        card = Card.objects.get(customer=user,product = product)

        if card:
            if card.quantity<=1:
                card.delete()
            else:
                quantity = card.quantity - 1
                Card.objects.filter(pk=card.pk).update(quantity=quantity, amount=price * quantity)

        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect('login')

def deleteallcart(request,id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        user = request.user
        card = Card.objects.get(customer=user,product = product)

        if card:
            card.delete()

        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        return redirect('login')



def addToWish(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)
        user = request.user

        if Wishlist.objects.filter(product=product, customer=user).exists():
            print('already added')
        else:
            wishlist = Wishlist(product=product, customer=user)
            wishlist.save()

        return redirect('/')

    else:
        return redirect('login')


def showWish(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(customer=request.user)
        return render(request, 'wishlist.html', {'wishlist': wishlist})
    else:
        return redirect('login')


def search_result(request):
    keyword = request.GET.get("search")
    if len(keyword) > 0:
        searching_result = Product.objects.filter(name__contains=keyword)
        if len(searching_result) > 0:
            return render(request, "shop-grid.html", {"products": searching_result})
        else:
            errors =["Product not Found","Invalid Keyword"]
            return render(request, "errorpage.html", {"errors": errors})
    else:
        return redirect('/')

def category(request,tag):
    product = Product.objects.filter(tag =tag)
    if len(product)>0:
        return render(request, "shop-grid.html", {"products": product})
    else:
        errors = ["Product not Available","Thanks for your interest","Stock will available soon"]
        return render(request,'errorpage.html',{'errors':errors})





def about(request):
    category = (
        ('pitol', 'Pitol'),
        ('dinner', 'Dinner Set'),
        ('plastic', 'Plastic'),
        ('cooker', 'Cooker'),
    )
    # for rendering all products
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # for managing card and total calculation
    card = []
    cardCount = 0
    cardTotal = 0
    if request.user.is_authenticated:
        card = Card.objects.filter(customer=request.user)
        for crd in card:
            cardCount += 1
            cardTotal += crd.amount

    return render(request, 'shop-grid.html',
                  {'page_obj': page_obj, 'card': card, 'cardCount': cardCount, 'cardTotal': cardTotal,
                   'category': category})


def cart(request):
    card = []
    cardCount = 0
    cardTotal = 0
    if request.user.is_authenticated:
        card = Card.objects.filter(customer=request.user)
        for crd in card:
            cardCount += 1
            cardTotal += crd.amount
    return render (request,'cart.html',{'cards':card,'cardtotal':cardTotal})
