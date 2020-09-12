"""
Free Geocode for batch operation
"""

import datetime
import time
#Some free geocoders
from geopy.geocoders import Nominatim,AlgoliaPlaces,ArcGIS,GeocodeFarm
from geopy.exc import GeocoderUnavailable

#Free services, based on speed order provided
SERVICES = [Nominatim,AlgoliaPlaces,ArcGIS,GeocodeFarm]

class GeoCoder:
    """
    Class to help in geocoding operation
    May be cache later
    """
    def __init__(self, user_agent='blcalc'):
        self.count = 0 #make sure we don't over request them
        self.oldtime = datetime.datetime.now() - datetime.timedelta(0,2) #2 sec ago for first run
        self._user_agent=user_agent

    def fetch_geo(self, name):
        """
        Fetch geolocation from name
        :param str name: Location address
        :return: (latitude, longitude, name),
            None if not found
        """
        newtime = datetime.datetime.now()
        delta = newtime - self.oldtime
        #make slow request
        if self.count==0:
            self.oldtime = newtime
            if delta.seconds < 1:
                time.sleep(delta.microseconds/1000000)
        else: #We try to use order as possible
            if delta.seconds > 1: #elasped
                self.oldtime = newtime
                self.count=0 # Reset counter
        i = SERVICES[self.count]
        #change to new server
        result = None
        retries=0
        while result is None:
            if retries==len(SERVICES):
                break
            try:
                locator = i(user_agent=self._user_agent)
                location = locator.geocode(name)
                result = (location.latitude, location.longitude, name)
            except GeocoderUnavailable:
                print("Unable to connect, retrying")
            retries += 1
            self.count = (self.count+1)%len(SERVICES)
        return result

    def user_agent(self):
        """
        Returns user agent name
        """
        return self._user_agent
