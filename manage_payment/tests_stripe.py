from django.test import TestCase, RequestFactory
from django.conf import settings
from django.urls import reverse
from unittest.mock import patch, MagicMock

from manage_payment.stripe_payment import StripePayment
from manage_order.models import Order, Customer, Address # Assuming Address might be needed for full context later
from django.contrib.auth.models import User # Corrected import for User

class StripePaymentClassTests(TestCase):

    def setUp(self):
        # Create a dummy user and customer for order creation
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer')
        # Create a dummy address
        self.address = Address.objects.create(customer=self.customer, address_name='Home', address='123 Test St', mobile='1234567890')

        # Create a dummy order
        self.order = Order.objects.create(
            customer=self.customer,
            address=self.address,
            total_amount=100.00, # Example amount
            payment_status='Pending'
        )
        self.factory = RequestFactory()

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_success(self, mock_stripe_session_create):
        # Mock the Stripe API call
        mock_session_object = MagicMock()
        mock_session_object.id = 'cs_test_12345'
        mock_session_object.payment_status = 'unpaid'
        mock_stripe_session_create.return_value = mock_session_object

        # Prepare request for building URLs
        request = self.factory.get(reverse('stripe_config')) # Dummy request for build_absolute_uri

        stripe_payment = StripePayment(
            order_id=self.order.id,
            amount=self.order.total_amount,
            currency='usd',
            description='Test Payment',
            customer_email=self.customer.user.email
        )
        session = stripe_payment.create_checkout_session(request)

        self.assertIsNotNone(session)
        self.assertEqual(session.id, 'cs_test_12345')
        mock_stripe_session_create.assert_called_once()
        args, kwargs = mock_stripe_session_create.call_args
        self.assertEqual(kwargs['line_items'][0]['price_data']['unit_amount'], 10000) # 100.00 * 100
        self.assertEqual(kwargs['metadata']['order_id'], str(self.order.id))
        self.assertIn(f"stripe/success/{self.order.id}", kwargs['success_url'])
        self.assertIn(f"stripe/cancel/{self.order.id}", kwargs['cancel_url'])

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_stripe_error(self, mock_stripe_session_create):
        # Simulate a Stripe API error
        # We need to import stripe to reference stripe.error.StripeError
        import stripe
        mock_stripe_session_create.side_effect = stripe.error.StripeError("Stripe API Error")

        request = self.factory.get(reverse('stripe_config'))
        stripe_payment = StripePayment(
            order_id=self.order.id,
            amount=self.order.total_amount,
            currency='usd'
        )
        session = stripe_payment.create_checkout_session(request)

        self.assertIsNone(session)

    def test_create_checkout_session_missing_amount(self):
        request = self.factory.get(reverse('stripe_config'))
        stripe_payment = StripePayment(order_id=self.order.id, currency='usd')
        with self.assertRaises(ValueError):
            stripe_payment.create_checkout_session(request)

    @patch('stripe.Webhook.construct_event')
    @patch('manage_payment.stripe_payment.Order.objects.get')
    def test_handle_webhook_checkout_session_completed(self, mock_order_get, mock_construct_event):
        mock_event = MagicMock()
        mock_event.type = 'checkout.session.completed'
        mock_event.data.object.metadata = {'order_id': str(self.order.id)}
        mock_event.data.object.payment_status = 'paid'
        mock_event.data.object.payment_intent = 'pi_test_123'
        mock_construct_event.return_value = mock_event

        # Make mock_order_get return a fresh instance of the order for this test
        # or ensure the self.order is what it would look like when get is called.
        # For simplicity, we are ensuring it returns the instance we have.
        mock_order_instance = self.order
        # Reset status for this specific test run if needed, or use a new order.
        mock_order_instance.payment_status = 'Pending'
        mock_order_instance.transaction_id = None
        mock_order_instance.save() # Save reset state

        mock_order_get.return_value = mock_order_instance

        payload = "{}" # Dummy payload
        sig_header = "t=123,v1=abc" # Dummy signature
        webhook_secret = "whsec_test"

        event_obj, status_code = StripePayment.handle_webhook_event(payload, sig_header, webhook_secret)

        self.assertEqual(status_code, 200)
        self.assertIsNotNone(event_obj)
        mock_order_get.assert_called_once_with(id=self.order.id)

        # Refresh the instance from the database to confirm changes were saved
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.payment_status, 'Paid')
        self.assertEqual(updated_order.transaction_id, 'pi_test_123')


# Import stripe at the end of the class or inside methods if it causes issues at module level during tests
# For now, assuming it's fine due to @patch, but sometimes direct imports can be tricky with mocking.
# Moved stripe import into test_create_checkout_session_stripe_error where it's first needed for stripe.error
# No, it's better to have it at the top or here if it's used in multiple places.
# For now, let's ensure stripe is imported if stripe.error is to be used.
import stripe
# It was referenced in test_create_checkout_session_stripe_error without being imported in its scope.
# The original plan had it at the end, which is fine.
# Let's ensure it's available for the StripeError.
# The @patch('stripe.checkout.Session.create') already implies stripe module is somewhat known.
# However, stripe.error.StripeError needs explicit import of stripe.
# The provided code had 'import stripe' at the very end.
# I've moved it into the test_create_checkout_session_stripe_error for clarity where stripe.error is used.
# And also added it here to be safe for the class if other tests use it.
# Re-evaluating: The last line 'import stripe' is fine.

# The provided code had User model import from manage_user.models which is incorrect.
# Corrected to `from django.contrib.auth.models import User`
# In `test_handle_webhook_checkout_session_completed`, I've added a save after resetting order status
# and made sure to fetch the updated_order from DB for assertion.
# This ensures we are testing the state as saved by the method.
