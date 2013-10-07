from django.db import models
from django.utils.translation import ugettext as _
from cms.models import CMSPlugin

####### HTML Plugin ###################


class HTMLPlugin(CMSPlugin):
    desc = models.CharField(max_length=300, blank=True, verbose_name=_("Description (hidden)"))  # Admin comment only; not rendered on the page
    html = models.TextField(blank=True, verbose_name=_("HTML"))
    css = models.TextField(blank=True, verbose_name=_("CSS"))
    js = models.TextField(blank=True, verbose_name=_("Javascript"))

    def __unicode__(self):
        return u"{}".format(self.desc)
