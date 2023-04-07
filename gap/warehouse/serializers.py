from rest_framework import serializers

from warehouse.models import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id", "location", "get_container_type_display", "items"]
