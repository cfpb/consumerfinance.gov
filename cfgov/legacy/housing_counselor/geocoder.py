from __future__ import absolute_import, unicode_literals

from six import print_


def geocode_counselors(counselors, **kwargs):
    """Fill in missing latitude/longitude data for housing counselors."""
    return ZipCodeBasedGeocoder(**kwargs).geocode(counselors)


class ZipCodeBasedGeocoder(object):
    """Fill in missing latitude/longitude data using zipcode locations.

    This "geocoder" just takes a housing counselor zipcode and uses it to set
    its latitude/longitude coordinates, if not already set.

    The zipcodes object passed to the constructor must be a dictionary with
    5-digit zipcode string lookup and keys of float (latitude, longitude).
    """
    def __init__(self, zipcodes):
        self.zipcodes = zipcodes

    def geocode(self, counselors):
        return map(self.geocode_counselor, counselors)

    def geocode_counselor(self, counselor):
        counselor = dict(counselor)

        lat_lng_keys = ('agc_ADDR_LATITUDE', 'agc_ADDR_LONGITUDE')
        if all(counselor.get(k) is not None for k in lat_lng_keys):
            return counselor

        print_('need to geocode this counselor: ', counselor, flush=True)
        zipcode = counselor['zipcd'][:5]

        if zipcode not in self.zipcodes:
            raise KeyError('{} not in zipcodes'.format(zipcode))

        coordinates = self.zipcodes[zipcode]
        counselor.update(zip(lat_lng_keys, coordinates))

        return counselor
