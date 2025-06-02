import stripe
from django.conf import settings
from django.urls import reverse
from manage_order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePayment:
    def __init__(self, order_id=None, amount=None, currency='usd', description='Payment for order', customer_email=None):
        self.order_id = order_id
        self.amount = amount # Amount in cents
        self.currency = currency
        self.description = description
        self.customer_email = customer_email

    def create_payment_intent(self, request):
        if not self.amount or not self.order_id:
            raise ValueError("Amount and Order ID are required to create a payment intent.")

        try:
            # Convert amount to cents if it's not already
            amount_in_cents = int(self.amount * 100)

            success_url = request.build_absolute_uri(reverse('payment_success_stripe', args=[self.order_id]))
            cancel_url = request.build_absolute_uri(reverse('payment_cancel_stripe', args=[self.order_id]))

            intent_params = {
                'payment_method_types': ['card'],
                'amount': amount_in_cents,
                'currency': self.currency,
                'description': f"{self.description} #{self.order_id}",
                'metadata': {
                    'order_id': str(self.order_id),
                },
                # Using automatic_payment_methods
                # 'automatic_payment_methods': {'enabled': True}, # Option 1: Automatic
                # Or, using explicit payment method options for more control
                # 'payment_method_options': { # Option 2: Explicit (example for card)
                #     'card': {
                #         'request_three_d_secure': 'automatic'
                #     }
                # },
                # 'confirm': True, # Usually not confirmed here, but on the client-side
                # 'return_url': success_url, # For payment methods that require redirection
            }
            if self.customer_email:
                intent_params['receipt_email'] = self.customer_email

            payment_intent = stripe.PaymentIntent.create(**intent_params)
            return payment_intent
        except stripe.error.StripeError as e:
            # Handle Stripe errors (e.g., invalid request, API key issues)
            print(f"Stripe Error: {e}")
            return None
        except Exception as e:
            # Handle other errors
            print(f"An unexpected error occurred: {e}")
            return None

    def create_checkout_session(self, request):
        if not self.amount or not self.order_id:
            raise ValueError("Amount and Order ID are required to create a checkout session.")

        try:
            amount_in_cents = int(self.amount * 100)

            # Ensure URLs are correctly defined in your urls.py
            # The view names 'payment_success_stripe' and 'payment_cancel_stripe' must exist
            success_url = request.build_absolute_uri(reverse('payment_success_stripe', args=[self.order_id])) + '?session_id={CHECKOUT_SESSION_ID}'
            cancel_url = request.build_absolute_uri(reverse('payment_cancel_stripe', args=[self.order_id]))

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': self.currency,
                        'product_data': {
                            'name': f"Order #{self.order_id}",
                            'description': self.description,
                        },
                        'unit_amount': amount_in_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'order_id': str(self.order_id)
                },
                customer_email=self.customer_email if self.customer_email else None,
            )
            return session
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e.user_message}" if hasattr(e, 'user_message') else f"Stripe Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    @staticmethod
    def handle_webhook_event(payload, sig_header, webhook_secret):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            print(f"Invalid payload: {e}")
            return None, 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(f"Invalid signature: {e}")
            return None, 400

        # Handle the event
        if event.type == 'checkout.session.completed':
            session = event.data.object
            order_id = session.metadata.get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=int(order_id))
                    # Check if payment was successful
                    if session.payment_status == 'paid':
                        order.payment_status = 'Paid'
                        # You might want to store transaction_id from session.payment_intent
                        order.transaction_id = session.payment_intent
                        order.save()
                        print(f"Order {order_id} marked as paid.")
                    else:
                        order.payment_status = 'Failed' # Or some other status
                        order.save()
                        print(f"Payment for order {order_id} was not successful: {session.payment_status}")
                except Order.DoesNotExist:
                    print(f"Order with ID {order_id} not found.")
                except Exception as e:
                    print(f"Error updating order {order_id}: {e}")

        elif event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            order_id = payment_intent.metadata.get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=int(order_id))
                    order.payment_status = 'Paid'
                    order.transaction_id = payment_intent.id
                    order.save()
                    print(f"PaymentIntent for order {order_id} succeeded. Order marked as paid.")
                except Order.DoesNotExist:
                    print(f"Order with ID {order_id} not found for PaymentIntent.")
                except Exception as e:
                    print(f"Error updating order {order_id} from PaymentIntent: {e}")

        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            order_id = payment_intent.metadata.get('order_id')
            if order_id:
                try:
                    order = Order.objects.get(id=int(order_id))
                    order.payment_status = 'Failed'
                    order.transaction_id = payment_intent.id # Store failed attempt ID
                    order.save()
                    print(f"PaymentIntent for order {order_id} failed. Order status updated.")
                except Order.DoesNotExist:
                    print(f"Order with ID {order_id} not found for failed PaymentIntent.")
                except Exception as e:
                    print(f"Error updating order {order_id} from failed PaymentIntent: {e}")
        else:
            print(f'Unhandled event type {event.type}')

        return event, 200
