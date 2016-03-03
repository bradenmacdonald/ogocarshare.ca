"""
Integrate the Gift Certificates app with the Django admin site
"""
from django.contrib import admin
from .models import GiftCert


class GCAdmin(admin.ModelAdmin):
    """ Admin class for GiftCert """
    fields = (
        'order_date',
        'recipient_name',
        'amount',
        'from_name',
        'from_email',
        'from_phone',
        'paid',
        'applied_to_account',
        'confirmation_sent',
        'notes',
        'staff_notes',
    )
    list_display = (
        '__unicode__',
        'order_date',
        'paid',
        'applied_to_account',
        'confirmation_sent',
    )
    readonly_fields = ('order_date', 'notes', 'amount')

admin.site.register(GiftCert, GCAdmin)
