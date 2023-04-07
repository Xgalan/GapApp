from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Storage, Item
from partnumbers.models import Partnumber


class ItemInline(admin.TabularInline):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "partnumber":
            try:
                kwargs["queryset"] = Partnumber.objects.order_by("sku")
            except Partnumber.DoesNotExist:
                pass
        return super(ItemInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    model = Item
    fields = (
        "partnumber",
        "storage",
        "area",
    )
    fk_name = "storage"


class StorageAdmin(TreeAdmin):
    list_display = (
        "location",
        "container_type",
    )
    list_filter = ("container_type",)
    form = movenodeform_factory(Storage)
    inlines = [ItemInline]


admin.site.register(Storage, StorageAdmin)
