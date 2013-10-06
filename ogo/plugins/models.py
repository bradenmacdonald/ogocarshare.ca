from django.db import models
from cms.models import CMSPlugin
from django.core.validators import URLValidator
from filer.fields.image import FilerImageField


def _partner_logo_upload_to(inst, orig_filename):
    from django.template.defaultfilters import slugify
    ext = orig_filename.lower().rsplit('.',1)[-1]
    if ext not in ("jpg", "png", "jpeg", "gif"):
        ext = "img"
    return "partner-logos/{}.{}".format(slugify(inst.name), ext)

class Partner(CMSPlugin):

    name = models.CharField(max_length=128)
    link = models.CharField(max_length=255, blank=True, null=True, validators=[URLValidator(), ])
    logo = FilerImageField(null=False, blank=False)

    def __unicode__(self):
        return self.name

