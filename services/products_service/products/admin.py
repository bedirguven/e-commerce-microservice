from django.contrib import admin
from .models import Product

# Basit bir şekilde modeli kaydetmek
admin.site.register(Product)

# Daha fazla özelleştirme için ModelAdmin sınıfını kullanabilirsiniz
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'available')
    list_filter = ('available', 'category')
    list_editable = ('price', 'stock', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}  # Slug alanını ürün adına göre otomatik doldur

# Özelleştirilmiş ModelAdmin ile Product modelini kaydetme
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)