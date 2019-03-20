# 2018 - 2019 Imperial College London Biomedical Engineering Year 2 Engineering Design Project
# Ronald Hsu


import array
import urllib
import os
import struct
import RPi.GPIO as GPIO


Radius = 100
START_Y =51.4966478
START_X =-0.1736854
END_Y =51.5006107
END_X =-0.1640704
TOTAL_X_CAP =1016
TOTAL_Y_CAP =762
X_SCALE = abs(START_X - END_X)/TOTAL_X_CAP
Y_SCALE = abs(START_Y - END_Y)/TOTAL_Y_CAP
Long = (END_X - START_X) /2 + START_X
Lat = (END_Y - START_Y) /2 + START_Y
NUMBER_READOUTS = 3
name = [0,0,0,0,0,0]
ROAD_BUFFER = 50


GPIO.setmode(GPIO.BCM)
button_places = 23
button_roads = 16
button_exit = 27
GPIO.setup(button_places, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_roads, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print ("IP Adress for SSH:")
IP = os.system('hostname -I')
os.system('iwgetid')
print IP
os.system('espeak "Welcome to V I map" 2>/dev/null')
file = open( "/dev/input/mice", "rb" );
print ("PROGRAM LOADED!\n")



def places(channel):
        print ("LOADING DATABASE...")
        URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat)+","+str(Long)
        print URL, "\nPLACES DATABASE UPDATED!\n"
	print Lat
	print Long
        html=urllib.urlopen(URL)
        htmltext=html.read()
        postname = 1
        for i in range(NUMBER_READOUTS+1):
                phrase =  "\"name\" : \""
                prename = htmltext.find(phrase,postname)
                postname =  htmltext.find("\"", prename+len(phrase)+1)
                name[i] = htmltext[prename+len(phrase):postname]
                if name[i] == "l_attributions":
                        os.system('espeak "There are no more places nearby" 2>/dev/null')
                        break
                if i == 0:
                            os.system('espeak "{0}, {1} places within {2} metres" 2>/dev/null'.format(name[i],NUMBER_READOUTS,Radius))
                else:
                        print i,": ", name[i]
                        os.system('espeak "{0}" 2>/dev/null'.format(name[i]))
def exit(channel):
        print ("QUITING PROGRAM...\nIP Adress for SSH:")
        IP = os.system('hostname -I')
        wifi = os.system('iwgetid')
        os.system('espeak "IP Address {0}, wifi {1}" 2>/dev/null'.format(IP,wifi))
        raise SystemExit
def roads(channel):
        global Long
        global Lat
        URL_road = "https://roads.googleapis.com/v1/snapToRoads?&interpolate=true&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&path="
        #URL_road ="https://roads.googleapis.com/v1/nearestRoads?&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&points="
        for i in range(ROAD_BUFFER):
                print "GETTING ROAD DATA BUFFER...",i,"out of", ROAD_BUFFER
                buf = file.read(3)
                x,y = struct.unpack( "bb", buf[1:] );
                Long += x*X_SCALE
                Lat += y*Y_SCALE
                print ("Coord: x: %8f, y: %8f" % (Long, Lat));
                if i > 20:
                        URL_road += str(Lat)+","+str(Long)
                if i < ROAD_BUFFER-1 and i > 20:
                        URL_road += "|"
        print URL_road
        html=urllib.urlopen(URL_road)
        htmltext=html.read()
        print("ROAD SNAPPING LOADED!\n")
        postname = 1
        phrase =  "\"placeId\": \""
        prename = htmltext.find(phrase,postname)
        postname = htmltext.find("\"", prename+len(phrase)+1)
        placeId = htmltext[prename+len(phrase):postname]
        URL = "https://maps.googleapis.com/maps/api/place/details/json?&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&placeid="+placeId
        print "Place Id: ", placeId, "\n" , URL, "\nROAD NAME UPDATED!\n"
        html=urllib.urlopen(URL)
        htmltext=html.read()
        postname = 1
        phrase =  "\"formatted_address\" : \""
        prename = htmltext.find(phrase,postname)
        postname =  htmltext.find(",", prename+len(phrase)+1)
        road_address = htmltext[prename+len(phrase):postname]
        print("Road name: "),
        print(road_address)
        os.system('espeak "{0}" 2>/dev/null'.format(road_address))

GPIO.add_event_detect(button_places, GPIO.FALLING, callback=places, bouncetime=700)
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=exit, bouncetime=700)
GPIO.add_event_detect(button_roads, GPIO.FALLING, callback=roads, bouncetime=700)


while True:
        buf = file.read(3)
        x,y = struct.unpack( "bb", buf[1:] );
        Long += x*X_SCALE
        Lat += y*Y_SCALE
        print ("Coord: x: %8f, y: %8f" % (Long, Lat));


