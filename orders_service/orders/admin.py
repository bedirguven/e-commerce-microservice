from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Sipariş öğelerini (OrderItem) siparişle (Order) birlikte görüntüleme ve düzenleme.
    """
    model = OrderItem
    extra = 1  # Varsayılan olarak bir boş öğe eklenir
    readonly_fields = ('product', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    """
    Order modelinin admin panelindeki özelleştirilmiş görünümü.
    """
    list_display = ('id', 'customer', 'status', 'created_at', 'updated_at', 'total_price')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'customer__username', 'customer__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def total_price(self, obj):
        """
        Siparişin toplam fiyatını hesaplama.
        """
        return sum(item.price * item.quantity for item in obj.orderitem_set.all())
    total_price.short_description = 'Total Price'

# Order modelini özelleştirilmiş admin görünümü ile kaydetme
admin.site.register(Order, OrderAdmin)