"""
OGO's custom Django CMS plugins
"""
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from ogo.utils import cse_api
from ogo.vehicle_details.models import VehicleDetails
from .models import Partner, PageSection, BackgroundImage


class CarMapPlugin(CMSPluginBase):
    """
    Plugin that displays a map of all the cars in the fleet.
    """
    name = _("Map of all cars")
    render_template = "plugins/car_map.html"  # template to render the plugin with

    def render(self, context, instance, placeholder):
        context['plugin_id'] = instance.pk
        fleet_data = cse_api.get_fleet()
        all_car_ids = [car["id"] for loc in fleet_data["locations"].values() for car in loc['cars'].values()]
        live_availability = cse_api.get_availability(all_car_ids)
        context['car_count'] = fleet_data["car_count"]
        context['locations'] = fleet_data["locations"].values()
        context['locations_count'] = len(fleet_data["locations"])
        if live_availability:
            for loc in fleet_data["locations"].values():
                for car in loc['cars'].values():
                    if car["id"] in live_availability:
                        car["availability"] = live_availability[car["id"]]
        return context

plugin_pool.register_plugin(CarMapPlugin)


class CarListPlugin(CMSPluginBase):
    """
    Plugin that displays a list of all the cars, with pictures and live availability.
    """
    name = _("List of all cars")
    render_template = "plugins/car_list.html"  # template to render the plugin with

    def render(self, context, instance, placeholder):
        context['plugin_id'] = instance.pk
        car_details = {c.engage_id: c for c in VehicleDetails.objects.all()}
        fleet_data = cse_api.get_fleet()
        all_cars = []
        for loc in fleet_data["locations"].values():
            for car in loc['cars'].values():
                car["location"] = loc
                all_cars.append(car)
                if car["id"] in car_details:
                    car["description"] = car_details[car["id"]].description
                    car["image"] = car_details[car["id"]].image
        all_cars = sorted(all_cars, key=lambda car: car["id"])
        all_car_ids = [car["id"] for car in all_cars]
        live_availability = cse_api.get_availability(all_car_ids)
        context['car_count'] = fleet_data["car_count"]
        context['cars'] = all_cars
        context['locations'] = fleet_data["locations"].values()
        context['locations_count'] = len(fleet_data["locations"])
        if live_availability:
            for car in all_cars:
                if car["id"] in live_availability:
                    car["availability"] = live_availability[car["id"]]
            context["updated_time"] = live_availability["updated_at"]
        return context

plugin_pool.register_plugin(CarListPlugin)


class PartnerPlugin(CMSPluginBase):
    """
    Plugin that displays the logo of a partner name/organization
    """
    model = Partner
    name = _("Partner Logo")
    render_template = "plugins/partner.html"  # template to render the plugin with
    fields = ("name", "link", "logo")
    parent_classes = ['PartnerLogoSectionPlugin']
    require_parent = True

    def render(self, context, instance, placeholder):
        context.update({'partner': instance})
        return context

plugin_pool.register_plugin(PartnerPlugin)


class PageSectionPlugin(CMSPluginBase):
    """
    Plugin used to divide a long page of content into multiple sections

    Each section is displayed in a table of contents and allows direct-linking via an anchor
    """
    model = PageSection
    name = _("Page Section")
    render_template = "plugins/section.html"
    fields = ("title", "fragment_id", "show_header")
    allow_children = True

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'fragment_id': instance.fragment_id,
            'show_header': instance.show_header,
            'child_instances': instance.child_plugin_instances,
        })
        return context

plugin_pool.register_plugin(PageSectionPlugin)


class PartnerLogoSectionPlugin(PageSectionPlugin):
    """
    Section that holds partner logos and displays them in a grid.
    """
    name = _("Page Section with Partner Logos")
    render_template = 'plugins/section_partner_logos.html'
    child_classes = ['PartnerPlugin']

plugin_pool.register_plugin(PartnerLogoSectionPlugin)


class BackgroundImagePlugin(CMSPluginBase):
    """
    A plugin for displaying a large background image, with content in front of it.
    """
    model = BackgroundImage
    name = _("Background Image with Content")
    render_template = "plugins/background_image.html"
    fields = ("image", )
    allow_children = True

    def render(self, context, instance, placeholder):
        context.update({
            'image': instance.image,
            'child_instances': instance.child_plugin_instances,
        })
        return context

plugin_pool.register_plugin(BackgroundImagePlugin)
