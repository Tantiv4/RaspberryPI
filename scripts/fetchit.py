import requests
import time
import json
import urllib2
import sys
import subprocess
import os
import RPi.GPIO as GPIO

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
	time_out = time.time() + 120
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

#def get_ifttt_action(ip, port):
def get_ifttt_action(url):
	#url = "http://" + ip + ":" + port + "/action"
	print url
	req = urllib2.Request(url)
	req.add_header("Content-Type", "application/json")
	try:
		response = urllib2.urlopen(req).read()
		print response
		if response != "{}":
			response = json.loads(response)
			#print response
		status = response["status"]
		#print status
		if status == 200:
			action = response["response"]["event"]
			#print "action "  + action
		        
                        if action == "led":
				pin = response["response"]["pin"]
				led_toggle(pin)
			elif action == "gpio":
				pin = response["response"]["pin_num"]
				print "pin " + str(pin)
				ev_type = response["response"]["type"]
				#print "type " + ev_type
				if ev_type == "on":
					gpio_alert(pin, GPIO.HIGH)
				else:
					gpio_alert(pin, GPIO.LOW)
			elif action == "sms":
				phone = response["response"]["phone"]
				message = response["response"]["info"]
				print "sms is sent to configured number"
				# todo - use the actual maker channel details here in format
				# https://maker.ifttt.com/trigger/<your event>/with/key/<your maker channel key>
				ifttt_channel = ""
				sms_alert(ifttt_channel, phone, message)
			elif action == "mail":
				address = response["response"]["address"]
				message = response["response"]["message"]
				print "email is sent to configured address"
				# todo - use the actual maker channel details here in format
				# https://maker.ifttt.com/trigger/<your event>/with/key/<your maker channel key>
				ifttt_channel = ""
				email_alert(ifttt_channel, "send message " + message + "to " + address)
			else:
				print "event not configured"
		else:
			print "invalid response"
	except TypeError as error:
		print "Invalid response from server"
		print error 
	except urllib2.URLError:
		print "Unable to open the url"

# get response from ifttt and perform required action
#GPIO.setmode(GPIO.BOARD)
while True :
	try:
		#ip = sys.argv[1]
		#print ip
		#port = sys.argv[2]
		#print port
		#get_ifttt_action(ip, port)
		get_ifttt_action(sys.argv[1])
        	time.sleep(5)
	except KeyboardInterrupt:
		try:
			print os.system("killall node")
		except OSError as er:
			print er
		print "Exit FetchIT"
		sys.exit(0)

