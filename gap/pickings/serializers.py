from django.contrib.auth import get_user_model

from rest_framework import serializers

from pickings.models import Picking
from inspections.serializers import LotSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']


class PickingSerializer(serializers.ModelSerializer):
    picking_operator = UserSerializer()
    lot = LotSerializer()
    modified = serializers.DateTimeField(format='%d %b %Y')
    picking_date_display = serializers.DateField(source='picking_date', format='%d %b %Y')
    partnumber_display = serializers.ReadOnlyField(source='partnumber.sku')

    class Meta:
        model = Picking
        fields = ['id', 'partnumber', 'partnumber_display', 'lot', 'picking_date',
        'picking_operator', 'picking_date_display', 'created', 'modified']
