from django.db import models

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from filer.fields.image import FilerImageField


class FeatureImageExtension(PageExtension):
    """ Extend the CMS page model to add OGO-specific fields """
    feature_image = FilerImageField(blank=True)

extension_pool.register(FeatureImageExtension)
