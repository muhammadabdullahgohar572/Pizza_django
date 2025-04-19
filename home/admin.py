from django.contrib import admin
from .models import Pizza,PizzaCategory,cart,CartItems;


admin.site.register(Pizza)
admin.site.register(PizzaCategory)
admin.site.register(cart)
admin.site.register(CartItems)
