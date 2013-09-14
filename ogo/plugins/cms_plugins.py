from datetime import date
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin
from django.utils.translation import ugettext as _


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
