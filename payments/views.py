import hashlib
import hmac
import uuid
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer, VerifyPaymentSerializer, CreateOrderSerializer

logger = logging.getLogger(__name__)


def is_test_razorpay_credentials():
    key = getattr(settings, 'RAZORPAY_KEY_ID', '')
    secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    if not key or not secret:
        return True
    if key in ('your_key_id', 'your_key', 'YOUR_KEY_ID') or secret in ('your_key_secret', 'your_secret'):
        return True
    return False


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_paid:
            # Allow creating new payment orders if user wants to upgrade plans or buy extra features
            pass

        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan_name = serializer.validated_data.get('plan_name', 'lifetime')
        amount_inr = serializer.validated_data.get('amount_inr', 49)

        # Preset plan amounts if known plan
        if plan_name == 'lifetime':
            amount_inr = 49
        elif plan_name == 'pro':
            amount_inr = 199
        elif plan_name == 'enterprise':
            amount_inr = 499

        amount_paisa = amount_inr * 100

        # Check if using test/demo credentials
        if is_test_razorpay_credentials():
            mock_order_id = f"order_test_{uuid.uuid4().hex[:12]}"
            payment = Payment.objects.create(
                user=request.user,
                rzp_order_id=mock_order_id,
                amount_paisa=amount_paisa,
                plan_name=plan_name,
                status=Payment.STATUS_CREATED,
            )
            return Response({
                'order_id': mock_order_id,
                'amount': amount_paisa,
                'currency': 'INR',
                'key': 'rzp_test_demo_key',
                'payment_db_id': payment.id,
                'plan_name': plan_name,
                'is_test_mode': True,
                'detail': 'Sandbox Demo Mode active (Razorpay API credentials not configured in env).',
            }, status=status.HTTP_201_CREATED)

        try:
            import razorpay
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            order_data = {
                'amount': amount_paisa,
                'currency': 'INR',
                'payment_capture': 1,
                'notes': {
                    'user_email': request.user.email,
                    'plan_name': plan_name,
                }
            }
            order = client.order.create(data=order_data)

            payment = Payment.objects.create(
                user=request.user,
                rzp_order_id=order['id'],
                amount_paisa=amount_paisa,
                plan_name=plan_name,
                status=Payment.STATUS_CREATED,
            )

            return Response({
                'order_id': order['id'],
                'amount': amount_paisa,
                'currency': 'INR',
                'key': settings.RAZORPAY_KEY_ID,
                'payment_db_id': payment.id,
                'plan_name': plan_name,
                'is_test_mode': False,
            }, status=status.HTTP_201_CREATED)

        except ImportError:
            # Fallback to test mode if razorpay module missing
            mock_order_id = f"order_test_{uuid.uuid4().hex[:12]}"
            payment = Payment.objects.create(
                user=request.user,
                rzp_order_id=mock_order_id,
                amount_paisa=amount_paisa,
                plan_name=plan_name,
                status=Payment.STATUS_CREATED,
            )
            return Response({
                'order_id': mock_order_id,
                'amount': amount_paisa,
                'currency': 'INR',
                'key': 'rzp_test_demo_key',
                'payment_db_id': payment.id,
                'plan_name': plan_name,
                'is_test_mode': True,
                'detail': 'Razorpay SDK not installed. Running in Test Mode.',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Error creating Razorpay order: %s", str(e))
            return Response({'detail': f'Razorpay API error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rzp_order_id = serializer.validated_data['rzp_order_id']
        rzp_payment_id = serializer.validated_data['rzp_payment_id']
        rzp_signature = serializer.validated_data['rzp_signature']

        try:
            payment = Payment.objects.get(
                rzp_order_id=rzp_order_id,
                user=request.user,
            )
        except Payment.DoesNotExist:
            return Response(
                {'detail': 'Payment record not found for this user.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if payment.status == Payment.STATUS_SUCCESS:
            return Response({'message': 'Payment already verified.', 'is_paid': True, 'payment': PaymentSerializer(payment).data})

        # Test mode verification bypass
        if rzp_order_id.startswith('order_test_') or is_test_razorpay_credentials():
            payment.rzp_payment_id = rzp_payment_id or f"pay_test_{uuid.uuid4().hex[:12]}"
            payment.rzp_signature = rzp_signature or "test_signature_mock"
            payment.status = Payment.STATUS_SUCCESS
            payment.save()

            request.user.is_paid = True
            request.user.is_trial_active = False
            request.user.save(update_fields=['is_paid', 'is_trial_active'])

            return Response({
                'message': 'Test payment verified successfully. Account unlocked!',
                'is_paid': True,
                'is_test_mode': True,
                'payment': PaymentSerializer(payment).data,
            })

        # Production HMAC-SHA256 signature verification
        msg = f'{rzp_order_id}|{rzp_payment_id}'
        secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        generated_signature = hmac.new(
            secret.encode('utf-8'),
            msg.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(generated_signature, rzp_signature):
            payment.status = Payment.STATUS_FAILED
            payment.save(update_fields=['status'])
            return Response(
                {'detail': 'Invalid payment signature. Payment verification failed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment.rzp_payment_id = rzp_payment_id
        payment.rzp_signature = rzp_signature
        payment.status = Payment.STATUS_SUCCESS
        payment.save()

        request.user.is_paid = True
        request.user.is_trial_active = False
        request.user.save(update_fields=['is_paid', 'is_trial_active'])

        return Response({
            'message': 'Payment verified cleanly. Account unlocked!',
            'is_paid': True,
            'is_test_mode': False,
            'payment': PaymentSerializer(payment).data,
        })


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        return Response(PaymentSerializer(payments, many=True).data)


class PaymentReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk, user=request.user)
        except Payment.DoesNotExist:
            return Response({'detail': 'Invoice/Receipt not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'invoice_number': f"INV-SC-{payment.id:06d}",
            'date': payment.created_at.strftime('%B %d, %Y'),
            'user_email': payment.user.email,
            'user_name': getattr(payment.user, 'name', '') or payment.user.email,
            'plan_name': payment.plan_name.title(),
            'amount_rupees': payment.amount_rupees,
            'status': payment.status.title(),
            'rzp_order_id': payment.rzp_order_id,
            'rzp_payment_id': payment.rzp_payment_id or 'N/A',
            'merchant': 'SwipeCollab Inc.',
        })


class RazorpayWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
        if not webhook_secret:
            return Response({'status': 'ok'})

        signature = request.headers.get('X-Razorpay-Signature', '')

        generated = hmac.new(
            webhook_secret.encode('utf-8'),
            request.body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(generated, signature):
            return Response(
                {'detail': 'Invalid signature.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = request.data
        event = payload.get('event')

        if event == 'payment.captured':
            try:
                payment_entity = payload['payload']['payment']['entity']
                order_id = payment_entity.get('order_id')
                payment_id = payment_entity.get('id')

                payment = Payment.objects.get(rzp_order_id=order_id)
                if payment.status != Payment.STATUS_SUCCESS:
                    payment.rzp_payment_id = payment_id
                    payment.status = Payment.STATUS_SUCCESS
                    payment.save()
                    payment.user.is_paid = True
                    payment.user.is_trial_active = False
                    payment.user.save(update_fields=['is_paid', 'is_trial_active'])
            except Payment.DoesNotExist:
                pass
            except Exception as e:
                logger.exception("Webhook processing error: %s", str(e))

        return Response({'status': 'ok'})