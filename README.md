# magic_map_places_api
# VI Map by Group 12

- Network connection setup, crucial for HTTP request, and SSH script running

Raspi auto connects to any saved network in system config, when connecting to a new network, chosee one of the methods:
1.	Plug in HDMI and keyboard into Raspi
	Boot up
	“sudo raspi-config”
	Option 2
	Option N2
	Enter Wifi credentials
2.	Modify new Wifi credentials to match current saved networks (when no keyboard access to RasPi)
	SSID:	MM_HOTSPOT
	PW:		MM_PASSSWORD
3.	Plug in ethernet cable into the ethernet socket of Raspi if applicable


- Reboot Raspi with network already setup

(Note that in iPhones, hotspots will become undiscoverable after a period of time. To make sure Raspi can connect to the iPhone, connect a random device to the active iPhone hotspot, THEN turn on the Raspi)
1. Systems read “magic maps….”, ready to use
or
2. The script has not been set to run automatically.
  - This means either a keyboard or SSH mustbe used to run the script. The following session explains the SSH method but the counterpart should be similar.


- Running the script manually

1. Open an SSH program (Terminal.app in Mac OS recommended) and make sure it is on the same device as the RasPi.
2. The LOCALIPADDRESS of the Raspi has to be determined to SSH in, which can be found by runing a network scan app (Fing on iOS recommended)
3. type ssh pi@LOCALIPADDRESS, press yes, and then type raspberry as password
4. cd Magic_Maps_Imperial
5. python MM_HC.py for hardcoded South Ken map or MM_NFC.py for NFC maps (not recommended since sensor is not ready)
6. l.py is a script that loops the MM_HC.py script, it is useful for resseting the MM_HC.py with the pyshical button (which kills the MM_HC.py task)
7. A script can be made to run automatically by sudo nano /etc/rc.local


- Additional Info

The two airbars have a different orientaion when sensing, revert positivity of X_SCALE and Y_SCALE at the beginning of the script
Audio crashes from time to time, press ctril+c to kill it so the rest of the script can continue
