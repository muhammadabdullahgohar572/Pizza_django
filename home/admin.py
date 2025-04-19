from django.contrib import admin
from .models import Pizza,PizzaCategory,Cart,CartItems;


admin.site.register(Pizza)
admin.site.register(PizzaCategory)
admin.site.register(Cart)
admin.site.register(CartItems)
