from django.conf import settings
from django.db import models


class Payment(models.Model):
    STATUS_CREATED = "created"
    STATUS_PENDING = "pending"
    STATUS_SUCCESS = "success"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Created"),
        (STATUS_PENDING, "Pending"),
        (STATUS_SUCCESS, "Success"),
        (STATUS_FAILED, "Failed"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    AMOUNT_INR = 49

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    rzp_order_id = models.CharField(max_length=255, unique=True)
    rzp_payment_id = models.CharField(max_length=255, blank=True)
    rzp_signature = models.CharField(max_length=512, blank=True)
    amount_paisa = models.PositiveIntegerField(default=AMOUNT_INR * 100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments_payment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment #{self.pk} — {self.user.email} [{self.status}]"

    @property
    def amount_rupees(self):
        return self.amount_paisa / 100

    @property
    def is_successful(self):
        return self.status == self.STATUS_SUCCESS