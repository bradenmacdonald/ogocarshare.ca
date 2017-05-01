""" Views for OGO's gift certificates app """
from django.conf import settings
import django.forms as forms
from django.forms import ModelForm
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.template import RequestContext

from .models import GiftCert


class GCForm(ModelForm):
    """ Form for ordering a gift certificate """
    class Meta:
        fields = ("recipient_name", "from_name", "from_email", "from_phone", "amount", "notes")
        model = GiftCert
        widgets = {
            'amount': forms.TextInput(attrs={
                'placeholder': 'Enter dollar amount (do not include the $ sign)',
                'type': 'number',
                'step': '1',
                'min': '10',
                'max': '999',
            }),
        }


def order(request):
    """ Display and/or process the gift certificate order form """
    # Require that this page be accessed via HTTPS:
    if (not request.is_secure()) and settings.HTTPS_AVAILABLE:
        abs_url = request.build_absolute_uri(request.get_full_path())
        secure_url = abs_url.replace('http://', 'https://')
        return HttpResponsePermanentRedirect(secure_url)

    context = {}

    if request.method == 'POST':
        form = GCForm(request.POST)
        if form.is_valid():
            context['gc'] = form.save()
            return render(request, 'giftcert/paypal.html', context=context)
    else:
        form = GCForm()
    context['form'] = form

    return render(request, 'giftcert/order.html', context=context)


def complete(request):
    """ Display a "Your order is now complete" message """
    return render(request, 'giftcert/order_complete.html')
