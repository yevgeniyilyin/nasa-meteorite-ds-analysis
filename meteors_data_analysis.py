# Using NASA meteorite-landings dataset 
# https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh
import requests
from haversine import haversine, Unit
import math

# function for the list sorting
def get_dist(meteor):
    return meteor.get('distance', math.inf)
   
# download the dataset 
print("Loading NASA dataset...")
meteor_response = requests.get("https://data.nasa.gov/resource/gh4g-9sfh.json")
print("Loaded with the status_code " + str(meteor_response.status_code))

meteor_data = meteor_response.json()

# latitude and longitude for Stallikon
# find your own on https://www.findlatitudeandlongitude.com/
my_loc = (47.3202128, 8.4708176)

# calculate the distance between my_loc and each meteor landing site
for m in meteor_data:
    try:
        distance = haversine(my_loc, (float(m.get('reclat')), float(m.get('reclong'))))
    except:
        distance = math.inf
        print("Exception with {0}".format(m))
    finally:
        m.update({'distance':distance})
     

dist_treshold = int(input("Enter distance treshold: "))     
number_of_sites = len([m for m in meteor_data if m['distance'] <= dist_treshold])
     	
meteor_data.sort(key=get_dist)    
print("Found {0} landing sites within {1} km from you location:".format(number_of_sites, dist_treshold))
print(meteor_data[0:number_of_sites])	
