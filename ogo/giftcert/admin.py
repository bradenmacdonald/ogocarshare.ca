from datetime import datetime
from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import Http404, HttpResponseRedirect
from .models import GiftCert


class GCAdmin(admin.ModelAdmin):
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
