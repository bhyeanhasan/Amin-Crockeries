import reportlab.lib.colors
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.pdfbase.pdfmetrics import stringWidth

from .models import Wishlist, Cart, Order, OrderedItem
from manage_product.models import Product
from manage_user.models import Customer, Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from manage_user.views import sendMail
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor


def order(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('placed_at').reverse()
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

        # if float(total_amount) <= 0:
        #     messages.info(request, 'No items in your cart')
        #     return redirect('order')

        order = Order()
        order.customer = customer
        order.address = address
        order.payment_status = payment_status
        order.total_amount = total_amount
        order.save()

        html_content = render_to_string('component/email.html', {
            'name': customer.name,
            'order_id': order.id,
            'order_placed_at': order.placed_at,
            'order_total_amount': order.total_amount
        })

        text_content = strip_tags(html_content)

        send_mail(
            subject="Order Confirmation",
            message=text_content,
            html_message=html_content,
            from_email='oboyob16.official@gmail.com',
            recipient_list=[request.user.email],
        )

        # sendMail(request.user.email, "Order Placed",
        #          "Dear " + customer.name + "\n\n" +
        #          "Your order ID = " + str(order.id) + ", has been placed at " +
        #          str(order.placed_at) + "\nTotal amount = " + str(order.total_amount) + " BDT")

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

    if float(len(cart)) <= 0:
        messages.info(request, 'No items in your cart')
        return redirect('order')

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


def download_voucher(request, id):
    order = Order.objects.get(id=id)
    items = OrderedItem.objects.filter(order=order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;' + ' filename="Order_' + str(order.id) + '.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    fontname = 'Courier'
    fontsize = 10
    p.setFont(fontname, fontsize)
    p.drawString(40, height - 40, 'Order ID : ' + str(order.id))

    fontname = 'Courier'
    fontsize = 24
    text = "Amin Crockeries"
    p.setFont(fontname, fontsize)
    # p.setFillColor(HexColor(0xff8100))
    p.setFillColor(HexColor(0x800080))
    text_width = stringWidth(text, fontname, fontsize)
    p.drawString((width - text_width) / 2, height - 50, text)

    fontsize = 12
    text = "Doctor Potti Road, Jhalokathi"
    p.setFont(fontname, fontsize)
    text_width = stringWidth(text, fontname, fontsize)
    p.drawString((width - text_width) / 2, height - 70, text)

    fontsize = 12
    text = "Mobile: 01728253400 Email: bhyean@gmail.com"
    p.setFont(fontname, fontsize)
    text_width = stringWidth(text, fontname, fontsize)
    p.drawString((width - text_width) / 2, height - 85, text)

    p.setFillColor(HexColor(0x000000))

    fontsize = 14
    name = "Name : " + order.customer.name
    address = "Con No: " + order.address.mobile
    p.setFont(fontname, fontsize)
    text_width = stringWidth(address, fontname, fontsize)
    p.drawString(50, height - 110, name)
    p.drawString((width - 50 - text_width), height - 110, address)

    fontsize = 14
    address = "Address : " + order.address.address
    time = "Date : " + str(order.placed_at.date())
    p.setFont(fontname, fontsize)
    text_width = stringWidth(time, fontname, fontsize)
    p.drawString(50, height - 125, address)
    p.drawString((width - 50 - text_width), height - 125, time)

    p.line(40, height - 135, width - 40, height - 135)

    fontsize = 14
    p.setFont(fontname, fontsize)

    cnt = 1
    space = 155

    p.setFillColor(HexColor(0x0000EE))

    p.drawString(50, height - space, 'No')
    p.drawString(70, height - space, 'Product Name')
    p.drawString(320, height - space, 'Q * Unit Price')
    p.drawString(420, height - space, '    Price')

    p.setFillColor(HexColor(0x008000))

    space += 30
    for item in items:
        p.drawString(50, height - space, str(cnt))
        p.drawString(70, height - space, item.product.name[:25])
        p.drawString(320, height - space, str(item.quantity) + ' * ' + str(item.unit_price))
        p.drawString(420, height - space, ' =  ' + str(item.unit_price * item.quantity))
        p.drawString(width - 80, height - space, ' BDT ')
        cnt += 1
        space += 25

    p.line(300, height - space + 10, width - 40, height - space + 10)

    p.setFillColor(HexColor(0xef503b))

    p.drawString(320, height - space - 5, 'TOTAL AMOUNT')
    p.drawString(420, height - space - 5, ' =  ' + str(order.total_amount))
    p.drawString(width - 80, height - space - 5, ' BDT ')

    fontsize = 100
    fontname = 'Helvetica'
    p.setFont(fontname, fontsize)
    text = 'PAID'
    text_width = stringWidth(text, fontname, fontsize)
    p.setFillColorCMYK(0, 0, 0, 0.08)
    p.drawString((width / 2) - (text_width / 2), (height / 2) - 35, text)

    p.setStrokeColorCMYK(0, 0, 0, 0.08)
    p.ellipse((width / 2) - 180, (height / 2) - 70, (width / 2) + 180, (height / 2) + 70)
    p.ellipse((width / 2) - 182, (height / 2) - 71, (width / 2) + 182, (height / 2) + 71)

    p.showPage()
    p.save()
    return response


def wishList(request):
    wishListItems = Wishlist.objects.filter(customer__user=request.user)
    if len(wishListItems) <= 0:
        messages.info(request, 'No items in your wishlist')
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
        messages.info(request, 'Product added to Wishlist')
    else:
        messages.info(request, 'Product already in Wishlist')

    return redirect(request.META.get('HTTP_REFERER', '/'))


def deleteWishItem(request, id):
    wishItem = Wishlist.objects.get(id=id)
    wishItem.delete()
    messages.info(request, 'Successfully Deleted')
    return redirect("wishList")


def cart(request):
    cartitems = Cart.objects.filter(customer__user=request.user)
    if len(cartitems) <= 0:
        messages.info(request, 'No items in your cart')
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

    messages.info(request, 'Product added to Cart')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def deleteCartItem(request, id):
    cartItem = Cart.objects.get(id=id)
    if cartItem.quantity > 1:
        cartItem.quantity -= 1
        cartItem.save()
    else:
        cartItem.delete()
    messages.info(request, 'Successfully Deleted')
    return redirect("cart")
