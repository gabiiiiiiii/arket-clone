from django.urls import path
from django.urls import include, path

urlpatterns = [
    path('products', include('product.urls')),
    path('user', include('user.urls')),
    path('reviews', include('review.urls')),
    path('cart', include('cart.urls')),
]