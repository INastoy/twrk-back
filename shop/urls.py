from django.urls import path

from shop.api import ProductAPIView

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products'),
    path('products/<int:pk>/', ProductAPIView.as_view(), name='product'),
]
