from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
# Register your models here.


@admin.register(models.Category)
class CategoryAdmoin(admin.ModelAdmin):
    list_display = ['title', 'foods_count']
    search_fields = ['title']

    @admin.display(ordering='foods_count')
    def foods_count(self, category):
        url = (
            reverse('admin:restaurant_food_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, category.foods_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(foods_count=Count('food'))


@admin.register(models.Food)
class FoodAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'category']
    list_editable = ['unit_price']
    list_filter = ['category', 'last_update']
    list_per_page = 10
    #list_select_related = ['category']
    search_fields = ['title']
    @admin.display(ordering='inventory')
    def inventory_status(self, food):
        if food.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} foods were successfully updated',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership', 'orders']
    autocomplete_fields = ['user']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith',
                     'last_name__istartswith']  # "i" is short for insensitive

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        url = (
            reverse('admin:restaurant_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['food']
    model = models.OrderItem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields =['customer']
    inlines = [OrderItemInline]
    ordering = ['placed_at']

    list_display = ['id', 'placed_at', 'customer']
