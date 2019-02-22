from gpiozero import Button
import array
import urllib
import os
import struct

Radius = 100
START_Y =51.4966478
START_X =-0.1736854
END_Y =51.5006107
END_X =-0.1640704
TOTAL_X_CAP =1016
TOTAL_Y_CAP =762
X_SCALE = abs(START_X - END_X)/TOTAL_X_CAP
Y_SCALE = abs(START_Y - END_Y)/TOTAL_Y_CAP
NUMBER_READOUTS = 5
button = Button(23)
exit = Button (18)
name = [0,0,0,0,0,0]
Long = (END_X - START_X) /2 + START_X
Lat = (END_Y - START_Y) /2 + START_Y

print ("PROGRAM LOADED!\n")
print ("IP Adress for SSH:")
os.system('hostname -I')
os.system('iwgetid')
os.system('espeak "Welcome to V I map by Group 12" 2>/dev/null')
file = open( "/dev/input/mice", "rb" );
n_file = 0

while True:
    while (1): #n_file != file):
        print "1"
            buf = file.read(3)
            n_file = file
            x,y = struct.unpack( "bb", buf[1:] );
            #print x, y
            Long += x*X_SCALE
            Lat += y*Y_SCALE
            print ("Coord: x: %8f, y: %8f" % (Long, Lat));
            break
    if button.is_pressed:
        print ("LOADING DATABASE...")
        URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat)+","+str(Long)
        print URL
        html=urllib.urlopen(URL)
        htmltext=html.read()
        #htmltext = "TEST\"name\" : \"Imperial College London\",TESTTEST\"name\" : \"Museum\",TESTTEST\"name\" : \"NATAAAA\",TEST"
        print("DATABASE UPDATED!\n")
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
                start_flag = prename
                    os.system('espeak "{0}, Top {1} places within {2} metres are" 2>/dev/null'.format(name[i],NUMBER_READOUTS,Radius))
            else:
                print(i),
                print(": "),
                print(name[i])
                os.system('espeak "{0}" 2>/dev/null'.format(name[i]))
if exit.is_pressed:
    print ("Bye~")
    print ("IP Adress for SSH:")
    os.system('hostname -I')
    os.system('iwgetid')
    file.close()
        exit()

file.close()
