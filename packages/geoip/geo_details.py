import logging

logger = logging.getLogger(__name__)


class GeoDetails:
    """
    Geo location details class. Has attributes for:
    country_code, region, city and timezone.
    Special attribute geolocated tells whether the values were actually geo located or are
    values just default.
    """
    def __init__(self, geo_details):
        self.__dict__.update(geo_details)

    @classmethod
    def _get_etl_defaults(cls):
        return {'geolocated': False}

    @classmethod
    def _get_yap_defaults(cls):
        return {
            'country_code': None,
            'region': None,
            'city': None,
            'timezone': 'UTC',
            'zipcode': None,
            'latitude': None,
            'longitude': None,
            'accuracy_radius': None,
            'from_anonymous_proxy': None
        }

    @classmethod
    def _get_ysapi_defaults(cls):
        return GeoDetails({
            'zipcode': None,
            'country_code': None,
            'region': None,
            'city': None,
            'timezone': 'UTC',
            'geolocated': False
        })

    @classmethod
    def _get_gtapi_defaults(cls):
        return GeoDetails({
            'country_code': None,
            'region': None,
            'city': None,
            'timezone': 'UTC',
            'geolocated': False
        })

    @classmethod
    def get_defaults(cls, service):
        if service == "etl":
            return GeoDetails._get_etl_defaults()
        elif service == "yap":
            return GeoDetails._get_yap_defaults()
        elif service == "ysapi":
            return GeoDetails._get_ysapi_defaults()
        elif service == "gtapi":
            return GeoDetails._get_gtapi_defaults()

    @classmethod
    def get_located_details(cls, service, geo_match, anonymous_proxy):
        common_details = {
                            # in geolib2, an IP can have registered_country only
                            'country_code': geo_match.country.iso_code or geo_match.registered_country.iso_code,
                            'region': geo_match.subdivisions.most_specific.name,
                            'city': geo_match.city.name,
                            # geolib2 can return None as timezone
                            'timezone': geo_match.location.time_zone or 'UTC'
                         }

        if service == "etl":
            etl_details = {
                'zipcode': geo_match.postal.code,
                'latitude': geo_match.location.latitude,
                'longitude': geo_match.location.longitude,
                'accuracy_radius': geo_match.location.accuracy_radius,
                'is_anonymous_proxy': anonymous_proxy,
                'geolocated': True
            }
            return {**common_details, **etl_details}
        elif service == "yap":
            yap_details = {
                'zipcode': geo_match.postal.code,
                'latitude': geo_match.location.latitude,
                'longitude': geo_match.location.longitude,
                'accuracy_radius': geo_match.location.accuracy_radius,
                'from_anonymous_proxy': anonymous_proxy
            }
            return {**common_details, **yap_details}
        elif service == "ysapi":
            ysapi_details = {
                'zipcode': geo_match.postal.code,
                'geolocated': True,
            }
            return GeoDetails({**common_details, **ysapi_details})
        elif service == "gtapi":
            gtapi_details = {'geolocated': True}
            return GeoDetails({**common_details, **gtapi_details})
