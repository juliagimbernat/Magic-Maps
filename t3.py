# 2018 - 2019 Imperial College London Biomedical Engineering Year 2 Engineering Design Project
# Ronald Hsu

# features to be added for users
# wifi connection
# reboot wifi
# wpa_cli -i wlan0 reconfigure
# reboot app
# GSM
# tutorial speech and button
# soft ware update through USB

# recently added
# audio loudness
# speaker
# on/off button
# Write tag
# Read tag and auto update coordinates
# faster reboot


# Imports
import array
import urllib
import os
import struct
import RPi.GPIO as GPIO
import MFRC522

# GPIO setup
GPIO.setmode(GPIO.BCM)
button_places = 18
button_roads = 21
button_exit = 27
button_UP = 0
button_DOWN = 0
button_NFC = 0
GPIO.setup(button_places, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_roads, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_NFC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
MIFAREReader = MFRC522.MFRC522()

# Constant Variables
TOTAL_X_CAP = 1016
TOTAL_Y_CAP = 762
Radius = 100
#START_X = -0.1736854
#START_Y = 51.4966478
#END_X = -0.1640704
#END_Y = 51.5006107
NUMBER_READOUTS = 3
name = [0,0,0,0,0,0]
ROAD_BUFFER = 40
NFC_SCAN = true
KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
BLOCK_ADDRS = [8, 9, 10]


# Main function
print ("IP Adress for SSH:")
os.system('hostname -I')
os.system('iwgetid')
os.system('espeak "Welcome to V I map by Group 12" 2>/dev/null')
file = open( "/dev/input/mice", "rb" );
URL_road = "https://roads.googleapis.com/v1/snapToRoads?&interpolate=true&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&path="
#URL_road ="https://roads.googleapis.com/v1/nearestRoads?&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&points="
print ("PROGRAM LOADED!\n")

def vol_up(channel):
    #amixer scontrols
        amixer set PCM 1000+
def vol_down(channel):
        amixer set PCM 1000-
def wifi_add:
        SSID = raw_input(os.system('espeak "Enter Wifi name" 2>/dev/null'))
        PSK = raw_input(os.system('espeak "Enter Wifi password" 2>/dev/null'))
def wifi_add:
    NFC_SCAN = true

def places(channel):
        print ("LOADING DATABASE...")
        URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat)+","+str(Long)
        print URL, "\nPLACES DATABASE UPDATED!\n"
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
                            os.system('espeak "{0}, Top {1} places within {2} metres are" 2>/dev/null'.format(name[i],NUMBER_READOUTS,Radius))
                else:
                        print i,": ", name[i]
                        os.system('espeak "{0}" 2>/dev/null'.format(name[i]))
def exit(channel):
        print ("QUITING PROGRAM...\nIP Adress for SSH:")
        os.system('hostname -I')
        os.system('iwgetid')
        raise SystemExit
def roads(channel):
        global Long
        global Lat
        global URL_road
        for i in range(ROAD_BUFFER):
                print "GETTING ROAD DATA BUFFER...",i,"out of", ROAD_BUFFER
                buf = file.read(3)
                x,y = struct.unpack( "bb", buf[1:] );
                Long += x*X_SCALE
                Lat += y*Y_SCALE
                print ("Coord: x: %8f, y: %8f" % (Long, Lat));
                URL_road += str(Lat)+","+str(Long)
                if i < 49:
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
        phrase =  "\"long_name\" : \""
        prename = htmltext.find(phrase,postname)
        postname =  htmltext.find("\"", prename+len(phrase)+1)
        road_address = htmltext[prename+len(phrase):postname]
        print("Road name: "),
        print(road_address)
        os.system('espeak "{0}" 2>/dev/null'.format(road_address))

GPIO.add_event_detect(button_places, GPIO.FALLING, callback=places, bouncetime=700)
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=exit, bouncetime=700)
GPIO.add_event_detect(button_roads, GPIO.FALLING, callback=roads, bouncetime=700)
GPIO.add_event_detect(button_UP, GPIO.FALLING, callback=vol_up, bouncetime=700)
GPIO.add_event_detect(button_DOWN, GPIO.FALLING, callback=vol_down, bouncetime=700)
GPIO.add_event_detect(button_NFC, GPIO.FALLING, callback=NFC, bouncetime=700)



while true:
        while NFC_SCAN:
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                print "Card detected"
                    (status, uid) = MIFAREReader.MFRC522_Anticoll()
                    MIFAREReader.MFRC522_SelectTag(uid)
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 11, KEY, uid)
            data = []
            coord = ''
            if status == MIFAREReader.MI_OK:
                for block_num in BLOCK_ADDRS:
                    block = MIFAREReader.MFRC522_Read(block_num)
                    if block:
                        data += block
                    if data:
                        coord = ''.join(chr(i) for i in data)
                    MIFAREReader.MFRC522_StopCrypto1()
                    print coord
                    sep_pos_A = 0
                    separator =  ","
                    for i in range(4):
                        sep_pos_B =  coord.find(separator,sep_pos_A)
                        corner[i] = coord[sep_pos_A:sep_pos_B]
                        sep_pos_A = sep_pos_B
                        print i,": ", corner[i]
                    NFC_SCAN = false
                    START_X = corner[1]
                    START_Y = corner[2]
                    END_X = corner[3]
                    END_Y = corner[4]
                    X_SCALE = abs(START_X - END_X)/TOTAL_X_CAP
                    Y_SCALE = abs(START_Y - END_Y)/TOTAL_Y_CAP
                    Long = (END_X - START_X) /2 + START_X
                    Lat = (END_Y - START_Y) /2 + START_Y
        buf = file.read(3)
        x,y = struct.unpack( "bb", buf[1:] );
        Long += x*X_SCALE
            Lat += y*Y_SCALE
                print ("Coord: x: %8f, y: %8f" % (Long, Lat));

