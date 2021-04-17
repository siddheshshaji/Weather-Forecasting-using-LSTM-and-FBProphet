from django.contrib import admin
from .models import data_ny, data_dl, data_mum
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(data_ny)
@admin.register(data_dl)
@admin.register(data_mum)

class ViewAdmin(ImportExportModelAdmin):
    pass