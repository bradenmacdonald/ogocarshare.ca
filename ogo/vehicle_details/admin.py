"""
Integrate OGO's vehicle_details app with the Django admin site
"""
from django.contrib import admin
from .models import (
    VehicleDetails,
)


class VehicleDetailsAdmin(admin.ModelAdmin):
    """ Admin class for VehicleDetails """
    fields = ('name', 'engage_id', 'description', 'image')
    list_display = ('name', 'engage_id', 'description', 'has_image')
    readonly_fields = ('has_image', )


admin.site.register(VehicleDetails, VehicleDetailsAdmin)
