"""Defines URL patterns for store."""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login_form.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('view/<int:product_id>/', views.view, name='view'),
    path('checkout/', views.check_out, name='checkout'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('buy_now/<str:product_id>/<str:qty>', views.buy_now, name='buy_now'),
    path('process_order_now/', views.process_order_now, name='process_order_now'),
    path('product/create/', views.ProductCreate.as_view(), name='product_create')
]