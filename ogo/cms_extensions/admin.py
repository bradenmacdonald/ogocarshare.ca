"""
Classes to integrate OGO's CMS extensions with the Django admin.
"""
from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import FeatureImageExtension


class FeatureImageExtensionAdmin(PageExtensionAdmin):
    """ Admin class for FeatureImageExtension """

admin.site.register(FeatureImageExtension, FeatureImageExtensionAdmin)
