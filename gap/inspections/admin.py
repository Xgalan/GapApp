from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Lot


class LotResource(resources.ModelResource):
    class Meta:
        model = Lot
        fields = (
            "id",
            "lot_number",
            "lot_date",
            "supplier_type",
        )


class LotAdmin(ImportExportModelAdmin):
    resource_class = LotResource
    fields = (
        ("lot_number", "supplier_type"),
        "lot_date",
    )
    list_filter = (
        "supplier_type",
        "lot_date",
        "partnumbers",
    )
    list_display = (
        "id",
        "lot_number",
        "supplier_type",
        "lot_date",
    )
    raw_id_fields = ("partnumbers",)
    related_lookup_fields = {
        "m2m": ["partnumbers"],
    }


admin.site.register(Lot, LotAdmin)
