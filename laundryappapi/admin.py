# laundryappapi/admin.py

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('hp', 'nama', 'tanggal_masuk', 'tanggal_selesai', 'total_harga', 'status')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
