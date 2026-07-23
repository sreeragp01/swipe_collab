from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    amount_rupees = serializers.ReadOnlyField()
    is_successful = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = [
            'id', 'rzp_order_id', 'rzp_payment_id',
            'amount_paisa', 'amount_rupees',
            'status', 'is_successful',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields


class CreateOrderSerializer(serializers.Serializer):
    pass


class VerifyPaymentSerializer(serializers.Serializer):
    rzp_order_id = serializers.CharField()
    rzp_payment_id = serializers.CharField()
    rzp_signature = serializers.CharField()