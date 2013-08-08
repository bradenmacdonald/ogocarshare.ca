from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # The admin/backend site:
    url(r'^backend/', include(admin.site.urls)),
    # Anything else is handled by the CMS:
    url(r'^', include('cms.urls')),
)
