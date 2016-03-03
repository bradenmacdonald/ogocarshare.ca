"""
OGO's Django template context processors
"""
from django.conf import settings


def ogo_globals(_request):
    """
    Add some OGO global variables to the request context
    """
    return {
        'OGO_GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
    }
