from rest_framework import serializers

from inspections.models import Lot


class LotSerializer(serializers.ModelSerializer):
    lot_display = serializers.ReadOnlyField(source="__str__")
    text = serializers.ReadOnlyField(source="__str__")
    supplier_type_display = serializers.ReadOnlyField(
        source="get_supplier_type_display"
    )
    lot_date_display = serializers.DateField(
        source="lot_date", format="%d %b %Y", read_only=True
    )
    modified = serializers.DateTimeField(format="%d %b %Y", read_only=True)

    class Meta:
        model = Lot
        exclude = [
            "partnumbers",
        ]


class SingleLotSerializer(LotSerializer):
    picking_set = serializers.ReadOnlyField()
