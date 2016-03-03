"""
API client for Car Share Everywhere.

You must set CSE_API_ENDPOINT in your settings.
"""
from datetime import datetime
import logging

from django.conf import settings
from django.core.cache import cache
import requests

log = logging.getLogger(__name__)


def cse_api_query(path, cache_for_seconds=(4*60*60)):
    """ Query the CSE API, from cache if possible. """
    request_url = settings.CSE_API_ENDPOINT + path
    cache_key = 'cseapi:{}'.format(request_url)
    data = cache.get(cache_key)
    if data is None:
        try:
            log.debug("Fetching data from CSE API (%s)", path)
            data = requests.get(request_url).json()
            if isinstance(data, dict):
                data["retrieved_at"] = datetime.now()
        except Exception:
            log.exception("Unable to retrieve CSE API result for path '%s'", path)
            return None
        cache.set(cache_key, data, cache_for_seconds)
    return data


def get_fleet():
    """
    Get data about all the parking locations and cars in the fleet
    Returns None if there is a parse error.
    """
    raw_data = cse_api_query('/fleet/cars')
    try:
        # Go through the result, selecting which fields we want to expose
        # and fixing the type of various fields encoded as strings.
        locations = {}
        for n in raw_data["Neighbourhoods"].values():
            for loc in n["Locations"].values():
                l_id = int(loc['ID'])
                cars = {}
                for c in loc['Cars'].values():
                    c_id = int(c["ID"])
                    cars[c_id] = {
                        "id": c_id,
                        "year": int(c["Year"]) if "Year" in c else None,
                        "make": c.get("Make"),
                        "model": c.get("Model"),
                        "category": c.get("Category"),
                        "colour": c.get("Colour"),
                        "seats": int(c["Seats"]) if "Seats" in c else None,
                        "accessories": [a for a in c["Accessories"].values()] if c.get("Accessories") else [],
                    }
                locations[l_id] = {
                    "id": l_id,
                    "name": loc.get('Name', 'Location {}'.format(l_id)),
                    "lat": float(loc["Latitude"]) if "Latitude" in loc else None,
                    "lng": float(loc["Longitude"]) if "Longitude" in loc else None,
                    "short_description": loc.get('ShortDescription', ''),
                    "cars": cars,
                }
        fleet_data = {
            "car_count": int(raw_data["CarCount"]),
            "locations": locations,
        }
    except (ValueError, KeyError):
        log.exception("Error while parsing CSE API result.")
        return None
    return fleet_data


def get_availability(car_ids):
    """
    Get the current availability of the specified car.
    Data may be up to 15 minutes old.
    car_ids is an array of IDs to query.
    Returns a dict where the keys are the IDs of each car whose availability is known, plus
    "updated_at" which contains the date when the data was retrieved.
    """
    # Round the current time to the nearest half hour (bookings are made on the half hour)
    # e.g. Round 3:13PM to 3:00PM, 4:46PM to 5:00PM
    timestamp = round(datetime.now().timestamp()/(30*60))*30*60
    # Limit the query to 20 cars at a time maximum (see API documentation):
    car_ids = car_ids[:20]
    # Fetch the data from the API:
    car_ids_str = ",".join(str(car_id) for car_id in car_ids)
    raw_data = cse_api_query('/availability/{}?cars={}'.format(timestamp, car_ids_str))
    if not raw_data:
        return {}
    result = {}
    for entry in raw_data.get("Data", {}).values():
        try:
            car_id = int(entry["CarID"])
            if not entry["StartTime"]:
                # If StartTime == False, the car is not available at all during this time interval (the next 24 hours)
                result[car_id] = {"available": False, "available_soon": False}
            else:
                result[car_id] = {
                    "available": int(entry.get("StartTime")) == timestamp,
                    "available_soon": True,
                    "available_at": datetime.fromtimestamp(int(entry.get("StartTime"))),
                    "available_until": datetime.fromtimestamp(int(entry.get("EndTime"))),
                }
        except (ValueError, KeyError):
            log.exception("Error while parsing CSE API result.")
    result["updated_at"] = raw_data["retrieved_at"]
    return result
