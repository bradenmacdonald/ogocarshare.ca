from __future__ import division
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin
from django.utils.translation import ugettext as _
from ogo.utils import cse_api
from ogo.vehicle_details.models import VehicleDetails
from .models import Partner, PageSection


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
    model = Partner
    name = _("Partner Logo")
    render_template = "plugins/partner.html"  # template to render the plugin with
    fields = ("name", "link", "logo")

    def render(self, context, instance, placeholder):
        mtop = 0
        # Comute what sort of margin_top the template needs to use to
        # center the logo inside an area with a 2:1 ratio
        box_ratio = 2
        ratio = instance.logo._width / instance.logo._height
        if ratio > box_ratio:
            mtop = ((1 / box_ratio) - (1 / ratio)) / 2
        context.update({'partner': instance, 'mtop': mtop*100})
        return context

plugin_pool.register_plugin(PartnerPlugin)


class PageSectionPlugin(CMSPluginBase):
    model = PageSection
    name = _("Page Section")
    render_template = "plugins/section.html"
    fields = ("title", "fragment_id", "visible")

    def render(self, context, instance, placeholder):
        context.update({
            'title': instance.title,
            'fragment_id': instance.fragment_id,
            'visible': instance.visible,
        })
        return context

plugin_pool.register_plugin(PageSectionPlugin)
