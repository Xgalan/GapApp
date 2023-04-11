from django.contrib.auth import get_user_model

from rest_framework import serializers

from inspections.models import Lot
from warehouse.models import Storage
from partnumbers.models import Partnumber, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name", "created", "modified"]


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


class PartnumberSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    modified = serializers.DateTimeField(format="%d %b %Y")

    class Meta:
        model = Partnumber
        fields = [
            "id",
            "sku",
            "description",
            "get_unit_display",
            "unit",
            "pmu",
            "db_nr",
            "category",
            "created",
            "modified",
        ]


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "location", "get_container_type_display", "items"]
