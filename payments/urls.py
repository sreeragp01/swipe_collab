from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, PaymentHistoryView, RazorpayWebhookView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(),    name='payment-create-order'),
    path('verify/',       VerifyPaymentView.as_view(),  name='payment-verify'),
    path('history/',      PaymentHistoryView.as_view(), name='payment-history'),
    path('webhook/',      RazorpayWebhookView.as_view(), name='payment-webhook'),
]