#!/usr/bin/env python
from Queue import Queue
import getopt
import random
import sys
import json
import os
import threading
from coapthon import defines
from coapthon.client.coap import CoAP
from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.messages.request import Request
from coapthon.utils import parse_uri
import socket


client = None

coap_response = ""

def update_coap_response(response): # pragma: no cover
    coap_response = response

def get_coap_response(): # pragma: no cover
    return coap_response

def usage():  # pragma: no cover
    print "Command:\tcoapclient.py -o -p [-P]"
    print "Options:"
    print "\t-o, --operation=\tGET|PUT|POST|DELETE|DISCOVER|OBSERVE"
    print "\t-p, --path=\t\t\tPath of the request"
    print "\t-P, --payload=\t\tPayload of the request"
    print "\t-f, --payload-file=\t\tFile with payload of the request"


def client_callback(response):
    print "Callback"


def client_callback_observe(response):  # pragma: no cover
    global client
    print "Callback_observe"
    check = True
    while check:
        chosen = raw_input("Stop observing? [y/N]: ")
        if chosen != "" and not (chosen == "n" or chosen == "N" or chosen == "y" or chosen == "Y"):
            print "Unrecognized choose."
            continue
        elif chosen == "y" or chosen == "Y":
            while True:
                rst = raw_input("Send RST message? [Y/n]: ")
                if rst != "" and not (rst == "n" or rst == "N" or rst == "y" or rst == "Y"):
                    print "Unrecognized choose."
                    continue
                elif rst == "" or rst == "y" or rst == "Y":
                    client.cancel_observing(response, True)
                else:
                    client.cancel_observing(response, False)
                check = False
                break
        else:
            break


def coap_action(message):  # pragma: no cover
    global client
    op = None
    path = None
    payload = None
    device_id = None
    device_type  = None
    Sensor_data  = None
    log_at        = None
    payload_sensor = None
    payload_alarm = None
   
    for o, a in message:
        if o in ("-o", "--operation"):
            op = a
        elif o in ("-p", "--path"):
            path = a
        elif o in ("-P", "--payload"):
            payload = a
        elif o in ("-f", "--payload-file"):
          if  os.path.isfile('./a.json'):
            with open('a.json','r') as f:
                payload_sensor = json.load(f)
                f.close
          else: 
            usage()
            sys.exit()

          if os.path.isfile('./b.json'):
            with open('b.json','r') as f:
                payload_alarm = json.load(f)
                f.close
                print payload_alarm["alarm_type"]
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(2)

    if op is None:
        print "Operation must be specified"
        usage()
        sys.exit(2)

    if path is None:
        print "Path must be specified"
        usage()
        sys.exit(2)

    if not path.startswith("coap://"):
        print "Path must be conform to coap://host[:port]/path"
        usage()
        sys.exit(2)

    host, port, path = parse_uri(path)
    host = socket.gethostbyname(host)
    client = HelperClient(server=(host, port))
    if op == "GET":
        if path is None:
            print "Path cannot be empty for a GET request"
            usage()
            sys.exit(2)
        response = client.get(path)
        print response.pretty_print()
	return response.payload
        client.stop()
    elif op == "OBSERVE":
        if path is None:
            print "Path cannot be empty for a GET request"
            usage()
            sys.exit(2)
        client.observe(path, client_callback_observe)
        
    elif op == "DELETE":
        if path is None:
            print "Path cannot be empty for a DELETE request"
            usage()
            sys.exit(2)
        response = client.delete(path)
        print response.pretty_print()
	return response.payload
        client.stop()
    elif op == "POST":
		if path is None:
			print "Path cannot be empty for a POST request"
			usage()
			sys.exit(2)
		if(payload_sensor or payload_alarm) is None:
			print "Payload cannot be empty for a POST request"
			usage()
			sys.exit(2)
		elif payload_alarm != None:     

			device_id = payload_sensor["device_id"]   
			Sensor_data = payload_sensor["sensor_data"]
			device_type  = payload_sensor["sensor_type"]
			log_at       = payload_sensor["logged_at"]     
			sensor_payload = "{\"device_id\":\""+device_id+"\",\"sensor_type\":\""+device_type+"\",\"sensor_data\":\""+str(Sensor_data)+"\",\"logged_at\":\""+log_at+"\"}"
			response = client.post(path, sensor_payload)
			print response.pretty_print()
            #return response.payload

			device_id = payload_alarm["device_id"]
			alarm     = payload_alarm["alarm_type"]
			log_at    = payload_alarm["alarm_at"]
			alarm_payloads = "{\"device_id\":\""+device_id+"\",\"alarm_type\":\""+str(alarm)+"\",\"alarm_at\":\""+log_at+"\"}"
			print alarm_payloads
			response = client.post(path, alarm_payloads)
			print response.pretty_print()
			os.remove("b.json")
			return response.payload
		else:

			device_id = payload_sensor["device_id"]   
			Sensor_data = payload_sensor["sensor_data"]
			device_type  = payload_sensor["sensor_type"]
			log_at       = payload_sensor["logged_at"]     
			sensor_payload = "{\"device_id\":\""+device_id+"\",\"sensor_type\":\""+device_type+"\",\"sensor_data\":\""+str(Sensor_data)+"\",\"logged_at\":\""+log_at+"\"}"
			print payload
			response = client.post(path, sensor_payload)
			print response.pretty_print()
			return response.payload
	
			client.stop()
    elif op == "PUT":
        if path is None:
            print "Path cannot be empty for a PUT request"
            usage()
            sys.exit(2)
        if payload is None:
            print "Payload cannot be empty for a PUT request"
            usage()
            sys.exit(2)
        response = client.put(path, payload)
        print response.pretty_print()
	return response.payload
        client.stop()
    elif op == "DISCOVER":
        response = client.discover()
        print response.pretty_print()
        client.stop()
    else:
        print "Operation not recognized"
        usage()
        sys.exit(2)

    update_coap_response(response.payload) 

if __name__ == '__main__':  # pragma: no cover
    coap_action(message)
