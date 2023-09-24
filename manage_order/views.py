from django.shortcuts import render, redirect
from .models import Wishlist, Cart, Order, OrderedItem
from manage_product.models import Product
from manage_user.models import Customer, Address
from django.contrib.auth.decorators import login_required


def order(request):
    orders = Order.objects.filter(customer__user=request.user)
    orderItems = OrderedItem.objects.filter(customer__user=request.user)

    for order in orders:
        return render(request, 'order.html', {'orders': orders, 'orderItems': orderItems})


def orderConfirm(request):
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        payment_status = request.POST.get('payment_status')
        total_amount = request.POST.get('total_amount')
        address_id = request.POST.get('address')
        address = Address.objects.get(id=address_id)

        if float(total_amount) <= 0:
            return redirect('order')

        order = Order()
        order.customer = customer
        order.address = address
        order.payment_status = payment_status
        order.total_amount = total_amount
        order.save()

        carts = Cart.objects.filter(customer=customer)
        for cart in carts:
            orderItem = OrderedItem()
            orderItem.order = order
            orderItem.product = cart.product
            orderItem.customer = customer
            orderItem.quantity = cart.quantity
            orderItem.unit_price = cart.product.unit_price
            orderItem.save()
            cart.delete()
        return redirect('order')

    cart = Cart.objects.filter(customer__user=request.user)
    total_amount = 0
    for i in cart:
        total_amount += i.product.unit_price * i.quantity
    addresses = Address.objects.filter(customer__user=request.user)
    items = Cart.objects.filter(customer__user=request.user)

    return render(request, 'orderConfirm.html', {'total_amount': total_amount, 'addresses': addresses, 'items': items})


def orderDetails(request, id):
    order = Order.objects.get(id=id)
    items = OrderedItem.objects.filter(order=order)
    return render(request, 'orderDetails.html', {'order': order, 'items': items})


def wishList(request):
    wishListItems = Wishlist.objects.filter(customer__user=request.user)
    return render(request, 'wishlist.html', {'wishListItems': wishListItems})


@login_required
def addToWishList(request, id):
    product = Product.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)

    if not Wishlist.objects.filter(customer=customer, product=product).exists():
        wish = Wishlist()
        wish.product = product
        wish.customer = customer
        wish.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def deleteWishItem(request, id):
    wishItem = Wishlist.objects.get(id=id)
    wishItem.delete()
    return redirect("wishList")


def cart(request):
    cartitems = Cart.objects.filter(customer__user=request.user)
    return render(request, 'cart.html', {'cartitems': cartitems})


@login_required
def addToCart(request, id):
    product = Product.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)

    if Cart.objects.filter(customer=customer, product=product).exists():
        cart = Cart.objects.get(customer=customer, product=product)
        cart.quantity = cart.quantity + 1
        cart.save()
    else:
        cart = Cart()
        cart.product = product
        cart.customer = customer
        cart.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def deleteCartItem(request, id):
    cartItem = Cart.objects.get(id=id)
    if cartItem.quantity > 1:
        cartItem.quantity -= 1
        cartItem.save()
    else:
        cartItem.delete()
    return redirect("cart")
