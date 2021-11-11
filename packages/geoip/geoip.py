import logging
import os

import geoip2.database
import geoip2.errors
import maxminddb

from packages.ip import is_in_subnet
from .geo_details import GeoDetails

logger = logging.getLogger(__name__)

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

geodb_location = f"{PROJECT_DIR}/GeoIP2-City.mmdb"


class Geoip:
    """
    Provides geolocation based on service (etl, yap or ysapi) and IP address
    """
    def __init__(self, service, test_invalid_db=None):
        self.service = service

        try:
            if test_invalid_db:
                logger.info(f"GeoIP db location: {test_invalid_db}")
                self.geo_db = geoip2.database.Reader(test_invalid_db)
            else:
                self.geo_db = geoip2.database.Reader(geodb_location)
        except (FileNotFoundError, geoip2.errors.PermissionRequiredError, maxminddb.InvalidDatabaseError) as ex:
            self.geo_db = None
            logger.error(f"Failed to import GeoIP module: {str(ex)}")

        # some random shit (using dependency)
        if not is_in_subnet("10.6.6.6", "10.6.0.0/16"):
            raise ValueError("oh no!")

    def get_geo_data(self, ip):
        """
        Get geo data object for given IP address. If geo location was not available,
        defaults will be returned (check GeoData class for detecting this).

        @param ip - IP address that is geo located.

        @returns GeoDetails instance for given IP.
        """
        if not self.geo_db:
            return GeoDetails.get_defaults(self.service)

        try:
            geo_match = self.geo_db.city(ip)
        except (ValueError, geoip2.errors.AddressNotFoundError):
            return GeoDetails.get_defaults(self.service)

        if geo_match:
            if hasattr(geo_match.traits, 'is_anonymous_proxy'):
                anonymous_proxy = geo_match.traits.is_anonymous_proxy
            else:
                anonymous_proxy = False
            return GeoDetails.get_located_details(self.service, geo_match, anonymous_proxy)

        return GeoDetails.get_defaults(self.service)

