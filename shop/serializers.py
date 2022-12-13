from rest_framework import serializers

from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        ret = super(ProductSerializer, self).to_representation(instance)
        if ret.get('image'):
            path, extension = instance.image.name.rsplit('.', 1)
            ret['image'] = {
                'path': path,
                'formats': ['webp', extension]
                }
        return ret
