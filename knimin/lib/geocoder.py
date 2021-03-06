from collections import namedtuple
import requests
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent='biocore/labadmin')
Location = namedtuple('Location', ['input', 'lat', 'long', 'elev', 'city',
                      'state', 'postcode', 'country'])


def elevation(lat, lng):
    """Attempt to determine the elevation using open-elevation

    geopy unfortunately does not provide this service
    """
    elev_url = "https://api.open-elevation.com/api/v1/lookup?locations=%f,%f"
    req = requests.get(elev_url % (lat, lng),
                       headers={'User-Agent': 'biocore/labadmin'})

    if req.ok:
        payload = req.json()
        results = payload['results']
        result = results[0]
        return result['elevation']
    else:
        return None


def geocode(address):
    location = geolocator.geocode(address, addressdetails=True,
                                  timeout=30, language='en')

    if location is None:
        return Location(address, None, None, None, None, None, None, None)

    if 'address' not in location.raw:
        return Location(address, None, None, None, None, None, None, None)

    addressdetails = location.raw['address']
    country = addressdetails.get('country')
    city = addressdetails.get('city')
    state = addressdetails.get('state')
    postcode = addressdetails.get('postcode')

    lat = location.latitude
    lng = location.longitude
    elev = elevation(lat, lng)

    return Location(address, lat, lng, elev, city, state, postcode, country)
