""" URLs for OGO's gift certificates app """
from django.conf.urls import url
from ogo.giftcert import views

urlpatterns = [
    url(r'^complete$', views.complete, name='giftcert_complete'),
    url(r'^$', views.order, name='giftcert_order'),
]
