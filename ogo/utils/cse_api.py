"""
API client for Car Share Everywhere.

You must set CSE_API_ENDPOINT in your settings.
"""
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
import requests


def get_fleet():
    fleet_data = cache.get('cse_fleet')  # This is the cached result of a previous call to this function, if any
    endpoint_used = cache.get('cse_fleet_endpoint')
    result_date = cache.get('cse_fleet_fetched')

    if endpoint_used != settings.CSE_API_ENDPOINT:
        # The endpoint has changed. Invalidate any old data.
        cache.delete('cse_fleet')
        fleet_data = None

    if (not fleet_data) or (datetime.now() - result_date) > timedelta(hours=4):
        # Fetch new/updated fleet data and cache it:
        try:
            r = requests.get(settings.CSE_API_ENDPOINT + '/fleet/cars')
            new_data = r.json()
            # Go through the result, selecting which fields we want to expose
            # and fixing the type of various fields encoded as strings.
            locations = {}
            for n in new_data["Neighbourhoods"].values():
                for loc in n["Locations"].values():
                    l_id = int(loc['ID'])
                    cars = {}
                    for c in loc['Cars'].values():
                        c_id = int(c["ID"])
                        cars[c_id] = {
                            "id": c_id,
                            "year": int(c["Year"]),
                            "make": c["Make"],
                            "model": c["Model"],
                            "category": c["Category"],
                            "colour": c["Colour"],
                            "seats": int(c["Seats"]),
                            #"plate": c["Plate"],
                            "accessories": [a for a in c["Accessories"].values()] if c["Accessories"] else [],
                        }
                    locations[l_id] = {
                        "id": l_id,
                        "name": loc['Name'],
                        "lat": float(loc["Latitude"]),
                        "lng": float(loc["Longitude"]),
                        "short_description": loc['ShortDescription'],
                        "cars": cars,
                    }
            fleet_data = {
                "car_count": int(new_data["CarCount"]),
                "locations": locations,
            }
            cache.set('cse_fleet', fleet_data, None)
            cache.set('cse_fleet_endpoint', settings.CSE_API_ENDPOINT, None)
            cache.set('cse_fleet_fetched', datetime.now(), None)
        except ValueError as e:
            print(e)
            pass
        except KeyError as e:
            print(e)
            pass
    return fleet_data
