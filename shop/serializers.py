from rest_framework import serializers

from shop.models import Product, PropertyValue, PropertyObject


class PropertyObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyObject
        fields = '__all__'


class PropertyValueSerializer(serializers.ModelSerializer):
    property_object = PropertyObjectSerializer()

    class Meta:
        model = PropertyValue
        fields = ('value_string', 'property_object', 'value_decimal', 'code')


class ProductSerializer(serializers.ModelSerializer):
    properties = PropertyValueSerializer(many=True)

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
