from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.login_page, name="login"),
    path('register/', views.register_page, name='register'),
    path('add-cart/<str:pizza_uid>/', views.add_cart, name='add_cart'),
]