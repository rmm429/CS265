#!/usr/bin/env python

#import statements
import json
import sys
import math
import operator
import urllib
import random

def getLoc() :
   '''Returns some location in Phila.
   ( LAT, LONG ), in decimal degrees'''

   #Min and Max lat and long for Philadelphia
   min_lat = 39.9155802878
   max_lat = 40.1026872756
   min_long = -75.2388309423
   max_long = -74.9699425597

   lat_delta = max_lat - min_lat
   long_delta = max_long - min_long

   mult = 1000

   x = random.randint( 0, int(long_delta*mult) )
   y = random.randint( 0, int(lat_delta*mult) )

   return ( min_lat + y/float(mult) , min_long + x/float(mult) )

#URL of the SEPTA JSON
URL = "http://www3.septa.org/hackathon/Stops/?req1=23"

#Reading the JSON in from the URL
fin = urllib.urlopen(URL)
#Parsing the URL data as a JSON
data = json.load(fin)

#Getting the number of arguments during script call
arg_num = len(sys.argv)

#Initializing the current and total distance display value
cur_disp = 1
total_disp = ""

#If there is more than one argument, set that as the total display
if (arg_num > 1) :
   total_disp = str(sys.argv[1]) # Getting the argument from call time
   total_disp = int(total_disp.replace("-n", "")) # isolating the number
                                                  # from the rest of the
                                                  # argument

# If there was only one argument, then default the total display to 5                                         
else :
   total_disp = 5

#Calling the getLoc() function to get a random Philly location
pos = getLoc()
#Retrieving the current latitude from the generated position
cur_lat = pos[0]
#Retrieving the current longitude from the generated position
cur_lng = pos[1]
#Initializing the distance to 0
dist = 0

#Creating an empty dictionary that will contain the stations and their
#distances from the current location
stations_and_dist = dict()

# dist( (x, y), (a, b) ) = sqrt( |(x - a)^2| + |(y - b)^2| )

#Going through each station in the JSON data
for stations in data :

   #Getting the name of the stop
   sta_stopname = stations['stopname']
   #Getting the latitude of the stop
   sta_lat = stations['lat']
   #Getting the longitude of the stop
   sta_lng = stations['lng']

   #Calculating distance using the Euclidean distance formula
   dist = math.sqrt( abs(math.pow( (sta_lat - cur_lat), 2 ) ) + abs(math.pow( (sta_lng - cur_lng), 2 ) ) )

   #Typecasing the station information as a string, concatenating the
   #station information, and placing it all inside a string
   station_info = str(dist) + "\t" + str(sta_stopname) + "\t(" + str(sta_lat) +  "," + str(sta_lng) + ")"

   #Appending to the dictionary the station information as the key and the
   #distance from the current location as the value
   stations_and_dist[station_info] = dist

#Sorting the dictionary based on the values, which are the distances from
#the current location, to get stations in increasing order of distance
stations_and_dist_sorted = sorted(stations_and_dist, key=stations_and_dist.get)

#Displaying the stations based on distance from the current location one
#line at a time
for cur_station in stations_and_dist_sorted :
   if (cur_disp <= total_disp) : #only displaying however many lines was
                                 #specified by either the user or by
                                 #default
       print cur_station
       cur_disp = cur_disp + 1