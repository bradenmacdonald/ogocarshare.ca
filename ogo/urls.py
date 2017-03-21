""" URLs for the OGO website """
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import django.views

admin.autodiscover()

urlpatterns = [
    url(r'^gift-certificate/', include('ogo.giftcert.urls')),
    # The admin/backend site:
    url(r'^backend/', include(admin.site.urls)),
    # Tagging for djangocms-blog:
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    # Anything else is handled by the CMS:
    url(r'^', include('cms.urls')),
]

if settings.SERVE_MEDIA_FILES:
    # On development servers, we need to manually specify that the media files
    # should be served:
    prefix = settings.MEDIA_URL.strip('/') + '/'
    urlpatterns += [
        url(prefix + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
