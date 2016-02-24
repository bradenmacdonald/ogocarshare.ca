from django.contrib import admin
from .models import (
    VehicleDetails,
)


class VehicleDetailsAdmin(admin.ModelAdmin):
    fields = ('name', 'engage_id', 'description', 'image')
    list_display = ('name', 'engage_id', 'description', 'has_image')
    readonly_fields = ('has_image', )


admin.site.register(VehicleDetails, VehicleDetailsAdmin)
