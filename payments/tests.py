from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from payments.models import Payment

User = get_user_model()


class RazorpayPaymentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='payer_user',
            email='payer@example.com',
            password='testpassword123',
            is_verified=True,
            is_paid=False,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_order_lifetime_plan(self):
        url = reverse('payment-create-order')
        data = {'plan_name': 'lifetime'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertEqual(response.data['amount'], 4900)
        self.assertEqual(response.data['plan_name'], 'lifetime')

        payment = Payment.objects.get(rzp_order_id=response.data['order_id'])
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.amount_paisa, 4900)
        self.assertEqual(payment.status, Payment.STATUS_CREATED)

    def test_create_order_pro_plan(self):
        url = reverse('payment-create-order')
        data = {'plan_name': 'pro'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], 19900)
        self.assertEqual(response.data['plan_name'], 'pro')

    def test_verify_test_payment(self):
        # First create an order
        create_url = reverse('payment-create-order')
        order_res = self.client.post(create_url, {'plan_name': 'lifetime'}, format='json')
        order_id = order_res.data['order_id']

        verify_url = reverse('payment-verify')
        verify_data = {
            'rzp_order_id': order_id,
            'rzp_payment_id': 'pay_test_123456789',
            'rzp_signature': 'test_signature_mock',
        }
        response = self.client.post(verify_url, verify_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_paid'])

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_paid)
        self.assertFalse(self.user.is_trial_active)

        payment = Payment.objects.get(rzp_order_id=order_id)
        self.assertEqual(payment.status, Payment.STATUS_SUCCESS)
        self.assertEqual(payment.rzp_payment_id, 'pay_test_123456789')

    def test_payment_history_and_receipt(self):
        payment = Payment.objects.create(
            user=self.user,
            rzp_order_id='order_test_history_99',
            rzp_payment_id='pay_test_history_99',
            amount_paisa=4900,
            plan_name='lifetime',
            status=Payment.STATUS_SUCCESS,
        )

        history_url = reverse('payment-history')
        response = self.client.get(history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        receipt_url = reverse('payment-receipt', kwargs={'pk': payment.pk})
        receipt_res = self.client.get(receipt_url)
        self.assertEqual(receipt_res.status_code, status.HTTP_200_OK)
        self.assertEqual(receipt_res.data['invoice_number'], f"INV-SC-{payment.pk:06d}")
        self.assertEqual(receipt_res.data['amount_rupees'], 49.0)
