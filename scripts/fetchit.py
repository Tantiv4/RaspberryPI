import requests
import time
import json
import urllib2
import sys
import subprocess
import os
import getopt
import RPi.GPIO as GPIO
from coapclient import coap_action
from coapclient import update_coap_response
from coapclient import usage
from coapclient import get_coap_response

#path = "/home/t4pi12345/test_scripts/FetchIT/scripts/"
#if path not in sys.path:
#        sys.path.append(path)
request_status = 1
coap_message = ""

def put():    # pragma: no cover
    update_coap_response("")

def get():
    coap_message =  get_coap_response()

# send email
def email_alert(first, second):
        report = {}
        report["value1"] = first
        requests.post(second, data = report)

def gpio_alert(pin, value):
	print str(pin) + " " + str(value)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, value)
	time.sleep(10) 
	GPIO.cleanup()
	print "gpio action on pin " + str(pin) + " registered"

def gpio_request(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	val = GPIO.input(pin)
	GPIO.cleanup()
	return val

def led_toggle(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	time_out = time.time() + 10
	while time.time() < time_out:
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(pin, GPIO.LOW)
		time.sleep(1)
	GPIO.cleanup()
	print "led toggled successfully"
		
def sms_alert(maker, phone, message):
	requests.post(maker, data = phone + " " + message)
	print "SMS request received"

def send_ifttt_response(status, unique_id):
	if status == 1:
		return
	payload = ""
	if status == 1:
		payload = "Falied"
	else:
		payload = "Passed"
	uri_path = "coap://api.tantiv4.com/respberrypi/ifttt/" + unique_id
	opts, args = getopt.getopt(['-oPOST', '-p' + uri_path, '-P' + payload], 'o:p:P:')
	print coap_action(opts)

def get_ifttt_action(message):
	#print message
	if message.find("OK"):
		response = json.loads(message)
		#print response
		action_str = response["response"]
		#print action_str
		action = ""
		for i in range(len(action_str)):
			action_req = action_str[i]
			print action_req
			if action_req != "":
				try:
					uid = action_req["_id"]["$oid"]
					action = action_req["actionFields"]["action_details"]
					print action
					action = json.loads(action)
					source = action["source"]
					print source
				        request_status = 0
					if source == "FetchIT":
						button_id = action["button_id"]
						print button_id
                        			if button_id == 1:
							led_toggle(32)
						elif button_id == 2:
							gpio_alert(32, GPIO.LOW)
						elif button_id == 3:
							gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 4:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 5:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 6:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 7:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 8:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 9:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 10:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 11:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 12:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 13:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 14:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 15:
                                                        gpio_alert(32, GPIO.HIGH)
                                                elif button_id == 16:
                                                        gpio_alert(32, GPIO.HIGH)
						else:
							print "Wrong Button Id"
					elif source == "Flic":
						gpio_alert(32, GPIO.HIGH)
					elif source == "Stringfy":
						phone = action["phone"]
						message = action["message"]
						print "sms is sent to configured number"
						# todo - use the actual maker channel details here in format
						# https://maker.ifttt.com/trigger/<your event>/with/key/<your maker channel key>
						ifttt_channel = ""
						sms_alert(ifttt_channel, phone, message)
					elif source == "maker":
						address = action["address"]
						message = action["message"]
						print "email is sent to configured address"
						# todo - use the actual maker channel details here in format
						# https://maker.ifttt.com/trigger/<your event>/with/key/<your maker channel key>
						ifttt_channel = ""
						email_alert(ifttt_channel, "send message " + message + "to " + address)
					else:
						print "event not configured"
					send_ifttt_response(request_status, uid)
				except KeyError:
					print "key not found in json response"
			else:
				print "no action to be done"
	else:
		print "invalid response" 

# get response from ifttt and perform required action
try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload=",
                                                               "payload_file="])
except getopt.GetoptError as err:
        #print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
while True:
	print opts
	try:
		request_status = 1;
		coap_message = coap_action(opts)
		#get()
		get_ifttt_action(coap_message)
		#coap_message = ""
		#put()
        	time.sleep(5)
	except KeyboardInterrupt:
		try:
			print os.system("killall node")
		except OSError as er:
			print er
		print "Exit FetchIT"
		sys.exit(0)

