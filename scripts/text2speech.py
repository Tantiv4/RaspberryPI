from __future__ import print_function, unicode_literals
import sys
from sys import argv
from gtts import gTTS 
import os
import getopt
import time
import socket
import json
from threading import Thread
from random import choice
from coapclient import coap_action
from coapclient import update_coap_response
from coapclient import usage
from coapclient import get_coap_response

try:
    # Python 3
    from urllib.parse import quote
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
    print('Running as python 3')
except ImportError:
    # Python 2
    from urllib import quote
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
    print('Running as python 2')

import soco

coap_message = ""
def get_ip_address():
     ip_address = '';
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.connect(("8.8.8.8",80))
     ip_address = s.getsockname()[0]
     s.close()
     return ip_address
machine_ip = get_ip_address()
port = 8000

def text2speech():
	zone = soco.discover()
	tts = gTTS(text=" This is FetchIT, which makes your life simplified", lang='en')
	tts.save("hello.mp3")


class HttpServer(Thread):
    """A simple HTTP Server in its own thread"""

    def __init__(self, port):
        super(HttpServer, self).__init__()
        self.daemon = True
        handler = SimpleHTTPRequestHandler
        self.httpd = TCPServer(("", port), handler)

    def run(self):
        """Start the server"""
        print('Start HTTP server')
        self.httpd.serve_forever()

    def stop(self):
        """Stop the server"""
        print('Stop HTTP server')
        self.httpd.socket.close()


def add_random_file_from_present_folder(machine_ip, port, zone_name):
    """Add a random non-py file from this folder and subfolders to soco"""
    # Make a list of music files, right now it is done by collection all files
    # below the current folder whose extension does not start with .py
    # This will probably need to be modded for other pusposes.
    
    music_files = []
    print('Looking for music files')
    for path, dirs, files in os.walk('.'):
        for file_ in files:
            if not ((os.path.splitext(file_)[1].startswith('.py')) or (os.path.splitext(file_)[1].startswith('.json')) or (os.path.splitext(file_)[1].startswith('.js'))or (os.path.splitext(file_)[1].startswith('.conf')) or (os.path.splitext(file_)[1].startswith('.pyc')) or (os.path.splitext(file_)[1].startswith('.py.swp'))):
                music_files.append(os.path.relpath(os.path.join(path, file_)))
                print('Found:', music_files[-1])

    random_file = choice(music_files)
    print (random_file)
    # urlencode all the path parts (but not the /'s)
    random_file = os.path.join(
        *[quote(part) for part in os.path.split(random_file)]
    )
    print('\nPlaying random file:', random_file)
    netpath = 'http://{}:{}/{}'.format(machine_ip, port, random_file)
    print (netpath)
    for zone in soco.discover():
        if zone.player_name == zone_name:
            break
    print (zone.player_name)
    zone.clear_queue()
    number_in_queue = zone.add_uri_to_queue(netpath)
    number_in_queue_1 = zone.get_current_track_info()['playlist_position']
    number_in_queue_1 = int(number_in_queue_1)-1
    zone.play_from_queue(int(number_in_queue_1))
    #return zone.get_current_track_info()

def play_text(message):
    # Settings
    if message.find("OK") != -1:
         response = json.loads(message)
         #print response
         action_str = response["response"]
         print (action_str)
         if action_str["status"] == "1":
            text2speech()
           # machine_ip = '192.168.0.104'
           # port = 8000
            zone_name = 'Stue'  # Danish for living room
            # Setup and start the http server
            #server = HttpServer(port)
            #server.start()
            
            # When the http server is setup you can really add your files in
            # any way that is desired. The source code for
            # add_random_file_from_present_folder is just an example, but it may be
            # helpful in figuring out how to format the urls
            add_random_file_from_present_folder(machine_ip, port, zone_name)

            # Remember the http server runs in its own daemonized thread, so it is
            # necessary to keep the main thread alive. So sleep for 3 years.
            #time.sleep(300)
             #server.stop()
            
         else:
            print ("No Action trigger")
    else: 
         print ("no action trigger")
# get response from ifttt and perform required action
try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:p:P:f:", ["help", "operation=", "path=", "payload=",
                                                               "payload_file="])
except getopt.GetoptError as err:
        #print help information and exit:
        print (str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
def main():
    server = HttpServer(port)
    server.start()
   
    while True:
            try:
                 request_status = 1;
                 coap_message = coap_action(opts)
                 print (coap_message)
                 play_text(coap_message)
                 time.sleep(5)
                
            except KeyboardInterrupt:
                try:
                        server.stop()
                        print (os.system("killall node"))
                except OSError as er:
                        print (er)
                print ("Exit FetchIT")
                sys.exit(0)
		
    

main()

