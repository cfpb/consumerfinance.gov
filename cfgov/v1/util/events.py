from django.conf import settings

import requests


def get_venue_coords(city=None, state=None):
    # Default to Washington DC coordinates
    venue_coords = "-77.039628,38.898238"

    if not city or not state or not settings.MAPBOX_ACCESS_TOKEN:
        return venue_coords

    location = "{} {}".format(city, state)
    api = "https://api.mapbox.com/geocoding/v5/mapbox.places-permanent/"
    location_api_url = api + location + ".json"

    params = {"access_token": settings.MAPBOX_ACCESS_TOKEN}
    response = requests.get(location_api_url, params=params)

    if response.status_code != 200:
        return venue_coords

    try:
        geo_data = response.json()
        coordinates = geo_data["features"][0]["geometry"]["coordinates"]
        venue_coords = str(coordinates[0]) + "," + str(coordinates[1])
    except KeyError:
        pass

    return venue_coords
