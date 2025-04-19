from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.login_page, name="login"),
    path('register/', views.register_page, name='register'),
    path('add-cart/<pizza_uid>/', views.add_cart, name='add_cart'),
    path('cart/', views.cart, name='cart'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path("Order/",views.Oder,name="Order"),
    path('remove-item/<uuid:item_uid>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
]