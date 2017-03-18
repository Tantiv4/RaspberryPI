import requests
import json
import urllib2
import sys
import subprocess
import os
import glob
import RPi.GPIO as GPIO
import time
import getopt
from datetime import datetime
from coapclient import coap_action
from coapclient import update_coap_response
from coapclient import usage
from coapclient import get_coap_response

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'


user_temperature =int(sys.argv[1])
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

temp = 0;

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
        if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000
		temp_f = temp_c * 9 / 5 + 32
		temp = int(temp_c)
                print temp
		return int(temp_c)
def raise_alarm():

    temp_sensor = read_temp()
    if user_temperature == temp_sensor:
        set_alarm = 1
    else: 
        set_alarm = 0
    return set_alarm

def send_ifttt_response(temperature,date_time):
        with open("a.json", "w") as f:
	        json.dump({'device_id':sys.argv[2],'sensor_type':"0",'sensor_data':temperature, 'logged_at':date_time}, f, indent=0)
       # uri_path = "coap://api-dev.tantiv4.com:5683/event/sensor" 
        uri_path = "coap://api.tantiv4.com/event/sensor"
        opts, args = getopt.getopt(['-oPOST', '-p' + uri_path,'-f'+ "f"], 'o:p:f:')
        f.close
        print coap_action(opts)
        set_alarm_1 = raise_alarm()
        print set_alarm_1
        if set_alarm_1 == 1:
           send_alarm(raise_alarm(),time.strftime("%c"))
        
def send_alarm(alarm,date_time):
       with open("b.json","w") as f:
               json.dump({'device_id':sys.argv[2],'alarm_type':"1",'alarm_at':date_time,"alarm":alarm}, f, indent = 0)
      # uri_alarm_path = "coap://api-dev.tantiv4.com:5683/event/alarm"
       uri_alarm_path = "coap://api.tantiv4.com/event/alarm"
       opts,args = getopt.getopt(['-oPOST','-p'+ uri_alarm_path,'-f'+ "f"],'o:p:f:')
       f.close
       print coap_action(opts)
while True:
        try:

                send_ifttt_response(read_temp(),time.strftime("%c"))
               # send_alarm(raise_alarm(),time.strftime("%c"))
                time.sleep(2)
        except KeyboardInterrupt:
                try:
                        print os.system("killall node")
                except OSError as er:
                        print er
                print "Exit FetchIT"
                sys.exit(0)


