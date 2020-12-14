from django.contrib import admin
from .models import Order, OrderItem, Copoun


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)


@admin.register(Copoun)
class CopounAdmin(admin.ModelAdmin):
    list_display = ('percent', 'valid_from', 'valid_to', 'active')
    list_filter = ('active', 'percent')
