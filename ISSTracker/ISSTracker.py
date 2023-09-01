import json
import turtle
import time
import webbrowser
import geocoder
from skyfield.api import Topos, load
import urllib.request

url = "http://api.open-notify.org/astros.json" #the URL used to get the information about the astronauts
response = urllib.request.urlopen(url)
result = json.loads(response.read())#the content of response is loaded as a JSON object, which contains info about the astronauts

#opens a file named "iss.txt" where astronaut info and user coordinates will be placed
file = open("iss.txt", "w")

#write all the information about the astronauts and the user's coordinates
file.write("There are currently " + str(result["number"]) + " astronauts on the ISS\n")
people = result['people']


for p in people:
    file.write(p['name'] + " is on board" + "\n")
g = geocoder.ip('me')
file.write("Your current lat is " + str(g.lat)+"\n")
file.write("Your current long is " + str(g.lng))
file.close()
webbrowser.open("iss.txt")

#setting up the map dimension
screen = turtle.Screen()
screen.setup(946, 502)
screen.setworldcoordinates(-180, -90, 180, 90)

#import the image and position of the map and iss logo
screen.bgpic("map3.gif")
screen.register_shape("iss3.gif")
iss = turtle.Turtle()
iss.shape("iss3.gif")
iss.setheading(45)
iss.penup()

# Minimum altitude (degrees) for the ISS to be considered above the horizon 
threshold_altitude = 10.0  

while True:
    #gets the information about the ISS position and stores it as a JSON
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    lat = float(result['iss_position']['latitude'])
    lon = float(result['iss_position']['longitude'])

    observer_lat = lat
    observer_lon = lon

    ts = load.timescale()
    satellites = load.tle_file('https://www.celestrak.com/NORAD/elements/stations.txt')
    satellite = None
    for sat in satellites:
        if sat.name == 'ISS (ZARYA)':
            satellite = sat
            break
    if satellite is None:
        print("ISS TLE data not found")
        break

    #gets the altitde and azimuth of the ISS in relative to the user's longitude and latitude
    observer = Topos(observer_lat, observer_lon)
    difference = satellite - observer
    alt, az, _ = difference.at(ts.now()).altaz()

    altitude = alt.degrees
    azimuth = az.degrees

    #prints the latitude, latitude, altitude, and azimuth in relative to the user's location
    print("\n Latitude: " + str(lat))
    print(" Longitude: " + str(lon))
    print(" Altitude: " + str(altitude) + " degrees")
    print(" Azimuth: " + str(azimuth) + " degrees")

    #makes the ISS logo go to the live longitude and latitude 
    iss.goto(lon, lat)
    iss.pendown()
           

    time.sleep(1)
