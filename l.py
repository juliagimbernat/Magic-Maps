import RPi.GPIO as GPIO
import os
GPIO.setmode(GPIO.BOARD)
button_exit = 13 #15 #22 TRIGGERS NFC RE-READ
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def exit(channel):
        print ("QUITING PROGRAM...\nIP Adress for SSH:")
        IP = os.system('hostname -I')
        wifi = os.system('iwgetid')
	os.system('pkill -f MM_HC.py')
        raise SystemExit
        os.system('espeak "QUIT" 2>/dev/null')
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=exit, bouncetime=700)

while True:
	os.system('sudo python /home/pi/Magic_Maps_Imperial/MM_HC.py')
	print ("hi")
