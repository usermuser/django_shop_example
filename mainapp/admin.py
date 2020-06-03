from django.contrib import admin
from .models import ProductCategory, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)


