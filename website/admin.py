from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'name', 'email', 'phone_number', 'address', 'payment_method', 'total_price', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'address')
    ordering = ('-created_at',)
