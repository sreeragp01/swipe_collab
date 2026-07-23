from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display   = ['id', 'user', 'amount_rupees_display', 'status', 'rzp_order_id', 'rzp_payment_id', 'created_at']
    list_filter    = ['status']
    search_fields  = ['user__email', 'rzp_order_id', 'rzp_payment_id']
    ordering       = ['-created_at']
    readonly_fields = ['rzp_order_id', 'rzp_payment_id', 'rzp_signature', 'amount_paisa', 'created_at', 'updated_at']

    fieldsets = (
        ('User',      {'fields': ('user',)}),
        ('Razorpay',  {'fields': ('rzp_order_id', 'rzp_payment_id', 'rzp_signature')}),
        ('Payment',   {'fields': ('amount_paisa', 'status')}),
        ('Timestamps',{'fields': ('created_at', 'updated_at')}),
    )

    actions = ['mark_success', 'mark_failed']

    @admin.display(description='Amount (₹)')
    def amount_rupees_display(self, obj):
        return f'₹{obj.amount_rupees}'

    @admin.action(description='Mark selected payments as Success (manual override)')
    def mark_success(self, request, queryset):
        for payment in queryset:
            payment.status = Payment.STATUS_SUCCESS
            payment.save()
            payment.user.is_paid         = True
            payment.user.is_trial_active = False
            payment.user.save(update_fields=['is_paid', 'is_trial_active'])
        self.message_user(request, f'{queryset.count()} payments marked as success.')

    @admin.action(description='Mark selected payments as Failed')
    def mark_failed(self, request, queryset):
        updated = queryset.update(status=Payment.STATUS_FAILED)
        self.message_user(request, f'{updated} payments marked as failed.')