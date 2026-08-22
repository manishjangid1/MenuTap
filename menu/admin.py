from django.contrib import admin
from .models import Restaurant, Category, MenuItem, MenuItemPrice


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name", "slug")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "display_order")
    list_filter = ("restaurant",)
    search_fields = ("name",)


class MenuItemPriceInline(admin.TabularInline):
    model = MenuItemPrice
    extra = 1


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "display_order",
    )
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    inlines = [MenuItemPriceInline]


@admin.register(MenuItemPrice)
class MenuItemPriceAdmin(admin.ModelAdmin):
    list_display = ("item", "size", "price")
    list_filter = ("size",)
    search_fields = ("item__name", "size")