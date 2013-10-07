" An image plugin integrated with django-filer and Bootstrap 3 "
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField


class ImageSettings(CMSPlugin):
    image = FilerImageField(null=False, blank=False)
    alt_text = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=512, blank=True, null=False, validators=[URLValidator(), ])
    caption = models.TextField(blank=True)

    QUALITY_ORIG = 0
    QUALITY_HIGH = 1
    QUALITY_MED = 2
    QUALITY_LOW = 3
    QUALITY_CHOICES = (
        (QUALITY_ORIG, _('Original')),
        (QUALITY_HIGH, _('High (for full-page images)')),
        (QUALITY_MED, _('Medium (large images)')),
        (QUALITY_LOW, _('Low (best for smaller images shown in a side column)')),
    )
    quality = models.IntegerField(null=False, choices=QUALITY_CHOICES, default=QUALITY_MED)

    TEMPLATE_FIT_WIDTH = 0
    TEMPLATE_FLOAT_LEFT = 1
    TEMPLATE_FLOAT_RIGHT = 2
    TEMPLATE_MODE_CHOICES = (
        (TEMPLATE_FIT_WIDTH, _('Fit to width of container')),
        (TEMPLATE_FLOAT_LEFT, _('Float to the left')),
        (TEMPLATE_FLOAT_RIGHT, _('Float to the right')),
    )
    template = models.IntegerField(null=False, choices=TEMPLATE_MODE_CHOICES, default=TEMPLATE_FLOAT_RIGHT, verbose_name=_('Position'))

    frame = models.BooleanField(null=False, default=True, verbose_name=_("Border"))

    def __unicode__(self):
        return self.image.name
