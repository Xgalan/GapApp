from rest_framework import serializers

from .models import Order, Orderitem


class ProductSerializer(serializers.ModelSerializer):
    coc_view = serializers.ReadOnlyField(source='coc.coc')
    shipdate = serializers.ReadOnlyField(source='coc.shipdate')
    partnumber_view = serializers.ReadOnlyField(source='partnumber.partnumber')
    status_display = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Orderitem


class OrderSerializer(serializers.ModelSerializer):
    customer_display = serializers.ReadOnlyField(source='customer.name')
    items = ProductSerializer(source='orderitem_set', many=True)

    class Meta:
        model = Order
        fields = ('id', 'coc', 'orderdate', 'shipdate', 'customer', 'customer_display', 'items')


class CocSerializer(serializers.ModelSerializer):
    customer_display = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Order
        fields = ('id', 'coc', 'orderdate', 'shipdate', 'customer', 'customer_display')


class ItemSerializer(serializers.ModelSerializer):
    coc_display = serializers.ReadOnlyField(source='coc.coc')
    shipdate = serializers.ReadOnlyField(source='coc.shipdate')
    status_display = serializers.ReadOnlyField(source='get_status_display')
    customer = serializers.ReadOnlyField(source='coc.customer.name')

    class Meta:
        model = Orderitem
        fields = (
            'coc',
            'coc_display',
            'customer',
            'partnumber',
            'shipdate',
            'status',
            'status_display',
            'status_changed',
            'quantity'
            )