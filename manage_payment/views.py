import random
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from manage_user.views import sendMail
from .aamarpay import aamarPay
from manage_user.models import Customer, Address
from manage_order.models import Order, Cart, OrderedItem


def pay(request, orderId):
    order = Order.objects.get(id=orderId)
    amount = order.total_amount
    customerName = Customer.objects.get(id=order.customer_id).name
    customerEmail = request.user.email

    address = Address.objects.get(id=order.address_id)

    customerMobile = address.mobile
    customerAddress1 = address.address
    customerCity = address.district
    customerState = address.division
    customerPostCode = address.zipcode

    pay = aamarPay(isSandbox=True,
                   transactionAmount=amount,
                   transactionID=random.randint(100000000, 999999999),
                   customerName=customerName,
                   customerEmail=customerEmail,
                   customerMobile=customerMobile,
                   customerAddress1=str(orderId),
                   customerCity=customerCity,
                   customerState=customerState,
                   customerPostCode=customerPostCode)
    paymentpath = pay.payment()
    return redirect(paymentpath)


def payment_success(request):
    if request.method == 'POST':
        ok = request.POST['pay_status']
        ok = str(ok)
        return render(request,'payment_success.html', {'ok': ok})


def payment_check(request, id):
    id = str(id)
    store_id = "aamarpaytest"
    signature = "dbb74894e82415a2f7ff0ec3a97e4183"
    url = "https://sandbox.aamarpay.com/api/v1/trxcheck/request.php?request_id=" + id + "&store_id=" + store_id + "&signature_key=" + signature + "&type=json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    ok = response.text
    return render(request, 'payment_success.html', {'ok': ok})
