from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^complete$', 'ogo.giftcert.views.complete', name='giftcert_complete'),
    url(r'^$', 'ogo.giftcert.views.order', name='giftcert_order'),
)
