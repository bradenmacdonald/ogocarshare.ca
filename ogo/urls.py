from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^gift-certificate/', include('ogo.giftcert.urls')),
    # The admin/backend site:
    url(r'^backend/', include(admin.site.urls)),
    # Anything else is handled by the CMS:
    url(r'^', include('cms.urls')),
]

if settings.SERVE_MEDIA_FILES:
    import django.views
    # On development servers, we need to manually specify that the media files
    # should be served:
    prefix = settings.MEDIA_URL.strip('/') + '/'
    urlpatterns += [
        url(prefix + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
