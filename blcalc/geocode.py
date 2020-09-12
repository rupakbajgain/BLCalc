#Some free geocoders
from geopy.geocoders import Nominatim,AlgoliaPlaces,ArcGIS,GeocodeFarm
import datetime
import time

#Free services, based on speed order provided
services = [Nominatim,AlgoliaPlaces,ArcGIS,GeocodeFarm]
#make sure we don't over request them
count = 0

#2 sec ago for first run
oldtime=datetime.datetime.now() - datetime.timedelta(0,2)

def fetchGeo(name):
    global oldtime, count
    newtime = datetime.datetime.now()
    delta = newtime - oldtime
    #make slow request
    if count==0:
        oldtime = newtime
        if delta.seconds < 1:
            time.sleep(delta.microseconds/1000000)
    else:#We try to use order as possible
        if delta.seconds > 1:#elasped
            oldtime = newtime
            count=0 #Reset counter
    i = services[count]
    #change to new server
    result = None
    retries=0
    while result==None:
        if retries==len(services):
            break
        try:
            locator = i(user_agent='blcalc')
            #print(locator)
            location = locator.geocode(name)
            result = (location.latitude, location.longitude, name)
        except:
            pass
        retries += 1
        count = (count+1)%len(services)
    return result