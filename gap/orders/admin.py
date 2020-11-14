from django.contrib import admin

from .models import Order, Orderitem, Company
from partnumbers.models import Partnumber



class CompanyAdmin(admin.ModelAdmin):
    model = Company


class OrderitemInline(admin.TabularInline):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "partnumber":
            try:
                kwargs["queryset"] = Partnumber.objects.filter(
                    category__category_name='Prodotto Finito').order_by('sku')
            except Partnumber.DoesNotExist:
                pass
        return super(OrderitemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    model = Orderitem
    fields = ('partnumber', 'quantity', 'status')
    fk_name = "coc"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('coc', 'orderdate', 'shipdate', 'customer', 'modified')
    list_filter = ('customer', 'shipdate')
    search_fields = ('coc',)
    date_hierarchy = 'orderdate'
    inlines = [
        OrderitemInline,
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(Company, CompanyAdmin)