from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "customer_name", "created_at")
    search_fields = ("customer_name", "customer_email")
    list_filter = ("created_at",)
