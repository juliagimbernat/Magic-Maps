Fresh SD card setup
#1 Install Raspbian
https://downloads.raspberrypi.org/raspbian_lite_latest
#2 sudo raspi-config
    1. Auto log in console mode
    2. Localisation
    3. Enable SSH, SPI, I2C
    4. Hostname -I
    5. sudo nano /etc/rc.local
    6. HDMI sudo nano /boot/config.txt
#3 Install GitHub
sudo apt install git
sudo git clone https://github.com/rayrayronald/Magic_Maps_Imperial.git
#4 Download GPIOzero
sudo apt install python-gpiozero
#5 Install espeak
sudo apt-get install python-pip
sudo apt-get install espeak
sudo pip install pyttsx
#6 Install audio shield
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
