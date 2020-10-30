from django.contrib import admin

from .models import Picking



class PickingAdmin(admin.ModelAdmin):
    raw_id_fields = ('partnumber', 'lot',)
    related_lookup_fields = {
        'fk': ['partnumber', 'lot'],
    }
    list_filter = ('partnumber', 'lot',)
    list_display = ('partnumber', 'lot', 'picking_date',)


admin.site.register(Picking, PickingAdmin)
