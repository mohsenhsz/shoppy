from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug':('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    list_editable = ('price',)
    list_filter = ('available', 'created',)
    prepopulated_fields = {'slug':('name',)}
    raw_id_fields = ('category',) # show a magnifier for browse between categories
    actions = ('make_available',)

    def make_available(self, request, queryset):
        rows = queryset.update(available=True)
        self.message_user(request, f'{rows} updated')
    make_available.short_description = 'Make available'
