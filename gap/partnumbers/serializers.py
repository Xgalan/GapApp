from rest_framework import serializers

from partnumbers.models import Partnumber, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'created', 'modified']


class PartnumberSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    modified = serializers.DateTimeField(format='%d %b %Y')

    class Meta:
        model = Partnumber
        fields = ['id', 'sku', 'description', 'get_unit_display', 'unit', 'pmu', 'db_nr',
        'category', 'created', 'modified']