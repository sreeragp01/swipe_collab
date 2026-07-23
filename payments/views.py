import hashlib
import hmac

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .serializers import PaymentSerializer, VerifyPaymentSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_paid:
            return Response({'detail': 'You have already paid.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            import razorpay
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            order_data = {
                'amount': Payment.AMOUNT_INR * 100,
                'currency': 'INR',
                'payment_capture': 1,
            }
            order = client.order.create(data=order_data)

            payment = Payment.objects.create(
                user=request.user,
                rzp_order_id=order['id'],
                amount_paisa=Payment.AMOUNT_INR * 100,
                status=Payment.STATUS_CREATED,
            )

            return Response({
                'order_id': order['id'],
                'amount': Payment.AMOUNT_INR * 100,
                'currency': 'INR',
                'key': settings.RAZORPAY_KEY_ID,
                'payment_db_id': payment.id,
            }, status=status.HTTP_201_CREATED)

        except ImportError:
            return Response(
                {'detail': 'Razorpay package not installed. Run: pip install razorpay'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rzp_order_id   = serializer.validated_data['rzp_order_id']
        rzp_payment_id = serializer.validated_data['rzp_payment_id']
        rzp_signature  = serializer.validated_data['rzp_signature']

        # ✅ Correct HMAC-SHA256 signature verification
        msg = f'{rzp_order_id}|{rzp_payment_id}'
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            msg.encode('utf-8'),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(generated_signature, rzp_signature):
            return Response(
                {'detail': 'Invalid payment signature. Payment could not be verified.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payment = Payment.objects.get(
                rzp_order_id=rzp_order_id,
                user=request.user,
            )
        except Payment.DoesNotExist:
            return Response(
                {'detail': 'Payment record not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if payment.status == Payment.STATUS_SUCCESS:
            return Response({'message': 'Payment already verified.', 'is_paid': True})

        payment.rzp_payment_id = rzp_payment_id
        payment.rzp_signature  = rzp_signature
        payment.status         = Payment.STATUS_SUCCESS
        payment.save()

        request.user.is_paid         = True
        request.user.is_trial_active = False
        request.user.save(update_fields=['is_paid', 'is_trial_active'])

        return Response({
            'message': 'Payment verified. Account unlocked!',
            'is_paid': True,
        })


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        return Response(PaymentSerializer(payments, many=True).data)


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
        event   = payload.get('event')

        if event == 'payment.captured':
            try:
                payment_entity = payload['payload']['payment']['entity']
                order_id   = payment_entity.get('order_id')
                payment_id = payment_entity.get('id')

                payment = Payment.objects.get(rzp_order_id=order_id)
                if payment.status != Payment.STATUS_SUCCESS:
                    payment.rzp_payment_id = payment_id
                    payment.status         = Payment.STATUS_SUCCESS
                    payment.save()
                    payment.user.is_paid         = True
                    payment.user.is_trial_active = False
                    payment.user.save(update_fields=['is_paid', 'is_trial_active'])
            except Payment.DoesNotExist:
                pass
            except Exception:
                pass

        return Response({'status': 'ok'})