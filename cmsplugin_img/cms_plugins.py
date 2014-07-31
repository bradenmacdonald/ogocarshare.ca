from django.conf import settings
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
#from django.contrib import admin
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from .models import ImageSettings


class ImagePlugin(CMSPluginBase):
    model = ImageSettings
    name = _("Image")
    render_template = "cmsplugin_img/instance.html"  # template to render the plugin with
    admin_preview = False
    fields = ("image", "alt_text", "link", "caption", "template", "quality", "frame", )
    text_enabled = True

    def render(self, context, instance, placeholder):
        if instance.quality == ImageSettings.QUALITY_HIGH:
            img_url = get_thumbnailer(instance.image).get_thumbnail({'size': (1600, 1200)}).url
        elif instance.quality == ImageSettings.QUALITY_MED:
            img_url = get_thumbnailer(instance.image).get_thumbnail({'size': (800, 800)}).url
        elif instance.quality == ImageSettings.QUALITY_LOW:
            img_url = get_thumbnailer(instance.image).get_thumbnail({'size': (400, 500)}).url
        else:
            img_url = instance.image.url

        context.update({
            'img_url': img_url,
            'alt_text': instance.alt_text,
            'link': instance.link,
            'caption': instance.caption,
            'mode': instance.template,
            'frame': instance.frame,
            'FIT_WIDTH': ImageSettings.TEMPLATE_FIT_WIDTH,
            'FLOAT_LEFT': ImageSettings.TEMPLATE_FLOAT_LEFT,
            'FLOAT_RIGHT': ImageSettings.TEMPLATE_FLOAT_RIGHT,
        })
        return context

    def icon_src(self, instance):
        if instance.image:
            return get_thumbnailer(instance.image).get_thumbnail({'size': (64, 64)}).url
        return settings.STATIC_URL + "cmsplugin_img/default.png"

plugin_pool.register_plugin(ImagePlugin)
