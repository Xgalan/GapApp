from rest_framework import serializers

from inspections.models import Lot


class LotSerializer(serializers.ModelSerializer):
    lot_display = serializers.ReadOnlyField(source='__str__')
    supplier_type_display = serializers.CharField(source='get_supplier_type_display')

    class Meta:
        model = Lot
        exclude = ['partnumbers']