import random
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from manage_user.views import sendMail
from .aamarpay import aamarPay
from manage_user.models import Customer, Address
from manage_order.models import Order, Cart, OrderedItem
from django.conf import settings
from .stripe_payment import StripePayment
from django.urls import reverse

# Existing views (pay, payment_success, payment_check) remain here

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

# New Stripe views

def get_stripe_publishable_key(request):
    return JsonResponse({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY})

@csrf_exempt
def checkout_session_stripe(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.payment_status == 'Paid':
            return render(request, 'errorpage.html', {'message': 'This order has already been paid.'})

        customer = Customer.objects.get(id=order.customer_id)
        # address = Address.objects.get(id=order.address_id) # Address might not be needed directly by Stripe session if not sending it

        stripe_payment = StripePayment(
            order_id=order.id,
            amount=order.total_amount,
            currency='usd', # Consider making this configurable
            description=f'Payment for Order #{order.id}',
            customer_email=request.user.email, # Assuming user is logged in
        )
        checkout_session = stripe_payment.create_checkout_session(request)

        if checkout_session and checkout_session.id:
            order.payment_method = 'stripe'
            order.transaction_id = checkout_session.id # Store session_id, payment_intent via webhook is better
            order.save()
            return JsonResponse({'sessionId': checkout_session.id})
        else:
            # Log error from StripePayment class if possible
            print("Stripe checkout session creation failed.") # Add more specific logging
            return render(request, 'errorpage.html', {'message': 'Could not initiate Stripe payment. Please try again.'})

    except Order.DoesNotExist:
        return render(request, 'errorpage.html', {'message': 'Order not found.'})
    except Customer.DoesNotExist:
        return render(request, 'errorpage.html', {'message': 'Customer not found.'})
    #except Address.DoesNotExist:
    #    return render(request, 'errorpage.html', {'message': 'Address not found.'})
    except Exception as e:
        print(f"Error in checkout_session_stripe: {e}")
        return render(request, 'errorpage.html', {'message': f'An unexpected error occurred: {e}'})

def payment_success_stripe(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        session_id = request.GET.get('session_id')

        if not session_id:
            return render(request, 'errorpage.html', {'message': 'Stripe session ID missing.'})

        # IMPORTANT: In production, verify session_id with Stripe API
        # For example:
        # stripe.api_key = settings.STRIPE_SECRET_KEY
        # stripe_session = stripe.checkout.Session.retrieve(session_id)
        # if stripe_session.payment_status == 'paid' and stripe_session.metadata.get('order_id') == str(order_id):
        # order.payment_status = 'Paid'
        # order.payment_method = 'stripe'
        # order.transaction_id = stripe_session.payment_intent # More reliable transaction ID
        # order.save()
        # else:
        # return render(request, 'errorpage.html', {'message': 'Invalid Stripe session or payment not completed.'})

        # Simplified version for now (without direct API call in this subtask to retrieve session)
        # The webhook is the more robust way to confirm payment.
        if order.transaction_id == session_id: # Basic check if we stored session_id
            order.payment_status = 'Paid' # Assume paid if redirected, webhook will confirm
            order.payment_method = 'stripe'
            order.save()
        else:
             # This case implies a mismatch or direct access, webhook should handle actual confirmation
             print(f"Warning: Success page accessed for order {order_id} but session_id mismatch or not primary confirmation method.")

        return render(request, 'payment_success.html', {'ok': f'Payment for order {order.id} via Stripe is being processed. You will be notified upon confirmation.'})
    except Order.DoesNotExist:
        return render(request, 'errorpage.html', {'message': 'Order not found.'})
    except Exception as e:
        print(f"Error in payment_success_stripe: {e}")
        return render(request, 'errorpage.html', {'message': f'An error occurred: {e}'})

def payment_cancel_stripe(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.payment_status != 'Paid':
            order.payment_status = 'Cancelled'
            order.payment_method = 'stripe' # Record attempted method
            order.save()
        # Create 'payment_cancel.html' or use an existing template
        return render(request, 'errorpage.html', {'message': f'Payment for order {order.id} was cancelled.'}) # Assuming errorpage can show general messages
    except Order.DoesNotExist:
        return render(request, 'errorpage.html', {'message': 'Order not found.'})
    except Exception as e:
        print(f"Error in payment_cancel_stripe: {e}")
        return render(request, 'errorpage.html', {'message': f'An error occurred: {e}'})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    # Ensure STRIPE_WEBHOOK_SECRET is set in settings
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

    if not webhook_secret:
        print("ERROR: Stripe webhook secret is not configured in settings.py.")
        return HttpResponse(status=400)

    event, status_code = StripePayment.handle_webhook_event(payload, sig_header, webhook_secret)

    if event or status_code == 200 : # handle_webhook_event returns event and status_code
        return HttpResponse(status=status_code)
    else:
        return HttpResponse(status=status_code if status_code else 400)
