from django.db import models
from cms.models import CMSPlugin
from django.core.validators import URLValidator


def _partner_logo_upload_to(inst, orig_filename):
    from django.template.defaultfilters import slugify
    ext = orig_filename.lower().rsplit('.',1)[-1]
    if ext not in ("jpg", "png", "jpeg", "gif"):
        ext = "img"
    return "partner-logos/{}.{}".format(slugify(inst.name), ext)

class Partner(CMSPlugin):

    name = models.CharField(max_length=128)
    link = models.CharField(max_length=255, blank=True, null=True, validators=[URLValidator(), ])
    logo = models.ImageField(null=False, blank=False, upload_to=_partner_logo_upload_to, width_field='logo_w', height_field='logo_h')
    logo_w = models.IntegerField(null=True)
    logo_h = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

