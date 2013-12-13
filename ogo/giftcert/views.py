from django.conf import settings
import django.forms as forms
from django.forms import ModelForm
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import GiftCert

class GCForm(ModelForm):
    class Meta:
        fields = ("recipient_name", "from_name", "from_email", "from_phone", "amount", "notes")
        model = GiftCert
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Enter dollar amount (do not include the $ sign)', 'type': 'number', 'step': '1', 'min': '10', 'max': '999'}),
        }


def order(request):
    # Require that this page be accessed via HTTPS:
    if (not request.is_secure()) and settings.HTTPS_AVAILABLE:
        abs_url = request.build_absolute_uri(request.get_full_path())
        secure_url = abs_url.replace('http://', 'https://')
        return HttpResponsePermanentRedirect(secure_url)

    context = RequestContext(request)

    if request.method == 'POST':
        form = GCForm(request.POST)
        if form.is_valid():
            context['gc'] = form.save()
            return render_to_response('giftcert/paypal.html', context_instance=context)
    else:
        form = GCForm()
    context['form'] = form

    return render_to_response('giftcert/order.html', context_instance=context)

def complete(request):
    context = RequestContext(request)
    return render_to_response('giftcert/order_complete.html', context_instance=context)
