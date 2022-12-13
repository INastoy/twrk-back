from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from shop.models import Product, PropertyValue
from shop.serializers import ProductSerializer


class ProductAPIView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = Product.objects.prefetch_related(Prefetch('properties', queryset=PropertyValue.objects.select_related(
                                                                           'property_object'))).all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('status',)
    search_fields = ('sku', 'title')

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:  # Сделано для разветвления запросов между выводом одной модели и списка.
            # Альтернативное решение - разделение на два класса: generic.ListAPIView и generic.RetrieveAPIView

            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
