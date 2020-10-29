from rest_framework import serializers

from inspections.models import Lot


class LotSerializer(serializers.ModelSerializer):
    supplier_type_display = serializers.CharField(source='get_supplier_type_display')

    class Meta:
        model = Lot
        exclude = ['partnumbers']