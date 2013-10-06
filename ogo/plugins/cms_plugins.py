from __future__ import division
from datetime import date
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin
from django.utils.translation import ugettext as _
from .models import Partner


class CarMapPlugin(CMSPluginBase):
    name = _("Map of all cars")
    render_template = "plugins/car_map.djhtml"  # template to render the plugin with
    admin_preview = False

    def render(self, context, instance, placeholder):
        from ogo.utils import cse_api
        fleet = cse_api.get_fleet()
        context['plugin_id'] = instance.pk
        context['car_count'] = fleet['car_count']
        context['car_locations'] = fleet['locations'].itervalues()
        context['car_locations_count'] = len(fleet['locations'])
        return context

plugin_pool.register_plugin(CarMapPlugin)

class PartnerPlugin(CMSPluginBase):
    model = Partner
    name = _("Partner Logo")
    render_template = "plugins/partner.djhtml"  # template to render the plugin with
    admin_preview = False
    fields = ("name", "link", "logo")

    def render(self, context, instance, placeholder):
        mtop = 0
        # Comute what sort of margin_top the template needs to use to
        # center the logo inside an area with a 2:1 ratio
        box_ratio = 2
        ratio = instance.logo._width / instance.logo._height
        if ratio > box_ratio:
            print("\n{}".format(instance.link))
            print("height of small logo = W / ratio = W / {}".format(ratio))
            print("height of box = W / box_ratio = W / {}".format(box_ratio))
            print("difference in height = ")
            mtop = ((1 / box_ratio) - (1 / ratio)) / 2
        context.update({'partner': instance, 'mtop': mtop*100})
        return context

plugin_pool.register_plugin(PartnerPlugin)


#height of small logo = W / ratio
#height of box = W / box_ratio
#difference = (W / box_ratio) - (W / ratio)
#difference / 2 = ((W / box_ratio) - (W / ratio)) / 2
#top_margin / W = (2 / box_ratio) - (2 / ratio)