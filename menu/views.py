from django.shortcuts import render
from .models import Restaurant

from django.shortcuts import render
from .models import Restaurant


def menu_home(request):
    restaurant = Restaurant.objects.filter(is_active=True).first()

    if not restaurant:
        restaurant = Restaurant.objects.create(
            name="DAILY USE CAFE",
            slug="daily-use-cafe",
            is_active=True
        )

    categories = restaurant.categories.prefetch_related(
        "items__prices"
    ).order_by("display_order")

    return render(
        request,
        "menu/home.html",
        {
            "restaurant": restaurant,
            "categories": categories,
        }
    )