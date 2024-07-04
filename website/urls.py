from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('why/', views.why, name='why'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('wishlist-count/', views.wishlist_count, name='wishlist_count'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('contact/', views.contact, name='contact'),
    path('create-order/', views.create_order, name='create_order'),
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),
    
]
