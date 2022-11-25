from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib.contenttypes.admin import GenericTabularInline
from restaurant.admin import FoodAdmin, FoodImageInline
from restaurant.models import Food
from tags.models import TaggedItem
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields=['tag']
    model=TaggedItem

class CustomFoodAdmin(FoodAdmin):
    inlines = [TagInline,FoodImageInline]


admin.site.unregister(Food)
admin.site.register(Food,CustomFoodAdmin)
