                                                    README

Introduction:

The document explains the requirement and steps required for handling requests from Fetchitgo
device in local network without any internet with the help of Raspberry Pi device.

Raspberry Pi

Raspberry Pi device acts as a CoAP server/client with DTLS. The CoAP server running will get the
request from Fetchit and forward to Fetchitgo node available in node red community.

WiFi Router or Ethernet Switch

The router acts as DHCP server to assign IP address to Raspberry Pi and Gateway. It forms a local
network so that FetchitGo can control any devices connected to Raspberry Pi

FetchitGo Node

A node is created in node red repositories which gets the requests from Raspberry Pi and forwards
to requested device attached.Please download the supported files from <provide github link here>

Californium CoAP Source code

A CoAP server is instantiated in Raspberry Pi to get requests and send response to Fetchitgo device.
Californium code is used for this purpose.
Please download it from here
https://github.com/eclipse/californium

Installation:

sudo npm install node-red-contrib-fetchitgo



