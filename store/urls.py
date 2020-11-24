"""Defines URL patterns for store."""

from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:product_id>/', views.cart, name='add_cart')
]