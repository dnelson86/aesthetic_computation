from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

import json
import pickle
import urllib
import numpy as np

from os.path import isfile
from datetime import datetime
from geopy.geocoders import Nominatim

class Command(BaseCommand):
    """ Download and parse the AAS job register page, create JSON file."""

    baselink = "https://jobregister.aas.org"
    savepath = "/var/www/html/static/ac/"
    random_amp = 0.02 # in {lat,long} for multiple entries in one city

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # init geolocator
        np.random.seed(424242)
        geolocator = Nominatim(user_agent="aasjobmap_app", timeout=5)

        # load geocache
        noted_locations = []

        if isfile(self.savepath + "geocache.pickle"):
            with open(self.savepath + 'geocache.pickle', 'rb') as f:
                geocache = pickle.load(f)
        else:
            geocache = {}

        # retrieve/load aas website
        req = urllib.request.Request(self.baselink, headers={'User-Agent':'Mozilla/5.0'})
        lines = [line.decode('utf-8') for line in urllib.request.urlopen(req).readlines()]

        # save last updated date
        jobs = []
        jobs.append({"last updated":datetime.now().strftime("%d %B, %Y")})

        # process each line
        curtype = None

        for i, line in enumerate(lines):
            # identify category (progressively down the page)
            if 'Visiting and Non-tenure Faculty Positions' in line:
                curtype = "other"
            if 'Tenure and Tenure-track Faculty Positions' in line:
                curtype = "faculty"
            if 'Post-doctoral Positions and Fellowships' in line:
                curtype = "postdoc"
            if 'Pre-doctoral / Graduate Positions' in line:
                curtype = "other"
            # several others after, which are all also "other"

            # detect start of new ad
            if '<a href="/jobregister/ad/' not in line:
                continue

            # link and title on this line
            line = line.split('<a href="')[1]
            link = line.split('" hreflang="en">')[0]

            title = line.split('" hreflang="en">')[1].split('</a>')[0]

            # institute on next line
            institute = lines[i+1].split('views-field-field-institution">')[1].split("</td>")[0]
            institute = institute.strip()

            # location on next next line
            if 'locality' not in lines[i+2]:
                location_name = institute # not specified beyond this
            else:
                location_name = lines[i+2].split('<span class="locality">')[1]
                location_name = location_name.replace('</span>, <span class="administrative-area">', ', ')
                location_name = location_name.replace('</span>-<span class="administrative-area">', ', ')
                location_name = location_name.replace('</span> <span class="administrative-area">', ', ')
                location_name = location_name.replace('</span><br>','').strip()

            # any pecularities to hack before geolocating?
            if location_name[-12:] == ", California":
                location_name = location_name.replace(", California", ", CA")
            if ", CA" in location_name[-5:]: # ending in ", CA" or ", CA "
                location_name += ", USA" # otherwise re-located to various Canadian cities
            location_name = location_name.replace("Multiple Locations,","") # generalize
            if "---" in location_name and "Various Canadian" in institute:
                location_name = "Toronto, Canada"
            if "Garching near Munich" in location_name:
                location_name = "Garching, Germany"
            if "Berlin/" in location_name:
                location_name = "Berlin, Germany"
            if ("La Serena or" in location_name) or ("and La Serena" in location_name):
                location_name = "La Serena, Coquimbo"
            if "Versoix (between" in location_name:
                location_name = "Versoix, Switzerland"
            if "Huntsvulle" in location_name:
                location_name = "Huntsville, AL"
            if "Barcelona" in location_name:
                location_name = "Barcelona, Spain"
            if "Kg.s Lyngby" in location_name:
                location_name = "Lyngby, Copenhagen"
            if "Durham, Durham" in location_name:
                location_name = "Durham, UK" # not NC
            if " and " in location_name:
                location_name = location_name.split(" and ")[0] # first

            # geolocate to (latitude,longitude), caching
            if location_name in geocache:
                lat, lon = geocache[location_name].latitude, geocache[location_name].longitude

                # add small random perturbation to prevent marker overlap
                # better to always include, in case people spell the locations slightly differently
                if 1: #location_name in noted_locations:
                    lat += np.random.uniform(low=self.random_amp/5, high=self.random_amp)
                    lon += np.random.uniform(low=self.random_amp/5, high=self.random_amp)
            else:
                # try multiple times in case of timeout
                geofailed = True
                count = 0

                while geofailed and count < 10:
                    try:
                        geocache[location_name] = geolocator.geocode(location_name)
                        geofailed = False
                    except GeocoderTimedOut:
                        count += 1

                # failed, try a permutation
                if geocache[location_name] is None:
                    try:
                        geocache[location_name] = geolocator.geocode(location_name.split(",")[0])
                    except:
                        pass

                # still failed? give up, place in ocean
                if geocache[location_name] is None:
                    geocache.pop(location_name)
                    lat = 41.0 + np.random.uniform(low=self.random_amp, high=self.random_amp*10)
                    lon = -30.0 + np.random.uniform(low=self.random_amp, high=self.random_amp*10)
                else:
                    lat, lon = geocache[location_name].latitude, geocache[location_name].longitude

            if location_name not in noted_locations:
                noted_locations.append(location_name)

            # add job
            job = {'link':self.baselink + link,
                   'title':title,
                   'type':curtype,
                   'location':location_name,
                   'institute':institute,
                   'lat':lat,
                   'long':lon}

            jobs.append(job)
            #print(len(jobs), job['type'], job['institute'], job['location'])

        # save geocache and json
        with open(self.savepath + 'geocache.pickle', 'wb') as f:
            pickle.dump(geocache, f)

        # json
        with open(self.savepath + 'aasjobmap.json','w',encoding='utf-8') as f:
            json.dump(jobs, f, indent=4)

        print('AAS Job Scrape Done [%s] (%d jobs).' % (jobs[0]["last updated"],len(jobs)-1))
