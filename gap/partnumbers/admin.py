import uuid

from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Partnumber, Category



class PartnumberResource(resources.ModelResource):
    id = Field(attribute=str(uuid.uuid4()))

    class Meta:
        model = Partnumber
        exclude = ('created', 'modified', 'id',)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class PartnumberAdmin(ImportExportModelAdmin):
    resource_class = PartnumberResource
    list_display = ('sku', 'category',)
    list_filter = ('category',)


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'category_name',)



admin.site.register(Partnumber, PartnumberAdmin)
admin.site.register(Category, CategoryAdmin)
