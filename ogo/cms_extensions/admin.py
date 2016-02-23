from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import FeatureImageExtension


class FeatureImageExtensionAdmin(PageExtensionAdmin):
    pass

admin.site.register(FeatureImageExtension, FeatureImageExtensionAdmin)
