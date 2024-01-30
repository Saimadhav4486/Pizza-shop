from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import UserProfile, FoodItem, Cart, CartItem

admin.site.register(UserProfile)
admin.site.register(FoodItem)
admin.site.register(Cart)
admin.site.register(CartItem)