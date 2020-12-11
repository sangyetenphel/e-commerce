"""Defines URL patterns for store."""

from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('view/<int:product_id>', views.view, name='view'),
    path('checkout/', views.check_out, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order')
]