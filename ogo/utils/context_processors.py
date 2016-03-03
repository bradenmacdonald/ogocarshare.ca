from django.conf import settings


def ogo_globals(request):
    """
    Add some OGO global variables to the request context
    """
    return {
        'OGO_GOOGLE_ANALYTICS_ACCOUNT': settings.GOOGLE_ANALYTICS_ACCOUNT,
    }
