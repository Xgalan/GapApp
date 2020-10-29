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

    class Meta:
        model = Picking
        fields = ['id', 'partnumber', 'lot', 'picking_date', 'picking_operator',
        'created', 'modified']
