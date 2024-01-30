from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns= [
    path('', views.product_page, name='default'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('products', views.product_page, name='product_page'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.view_cart, name='view_cart'),
    path('update_quantity/<int:cart_item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart')
]