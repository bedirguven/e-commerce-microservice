from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    """
    Payment modelinin admin panelindeki özelleştirilmiş görünümü.
    """
    list_display = ('id', 'customer', 'order', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('customer__username', 'order__id', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Payment, PaymentAdmin)