from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('why/', views.why, name='why'),
    path('products/', views.products, name='products'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
]