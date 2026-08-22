from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to="restaurant_logos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        
        return f"{self.name} - ₹{self.price}"


class MenuItemPrice(models.Model):
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="prices"
    )
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("item", "size")
        ordering = ["price"]

    def __str__(self):
        return f"{self.item.name} - {self.size} - ₹{self.price}"