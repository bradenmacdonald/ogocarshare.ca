"""
DB models for OGO's Django CMS plugins
"""
from cms.models import CMSPlugin
from django.db import models
from django.core.validators import URLValidator
from filer.fields.image import FilerImageField


class Partner(CMSPlugin):
    """ Represents a company/organization that is a partner of OGO """
    name = models.CharField(max_length=128)
    link = models.CharField(max_length=255, blank=True, null=True, validators=[URLValidator(), ])
    logo = FilerImageField(null=False, blank=False)

    def __str__(self):
        return self.name


class PageSection(CMSPlugin):
    """
    Represents a section of a multi-section page
    """
    title = models.CharField(max_length=128)
    fragment_id = models.SlugField(
        verbose_name="ID", max_length=32, null=False, blank=False,
        default="main",
        help_text=(
            "A short, unique, no-spaces, word or phrase that will appear in the URL if people "
            "link directly to this section."
        ),
    )
    show_header = models.BooleanField(null=False, default=False)

    def __str__(self):
        return u"Section: {}".format(self.title)


class BackgroundImage(CMSPlugin):
    """
    A plugin for displaying a large background image, with content in front of it.
    """
    image = FilerImageField(null=False, blank=False)
