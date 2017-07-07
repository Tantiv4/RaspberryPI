                                             README

Introduction:
        The document explains the requirement and steps required for 
handling requests from Fetchitgo device in local network without any 
internet with the help of Raspberry Pi device. 

About Fetchitgo:

          Fetchit will communicate to a CoAP server running in a 
Raspberry PI device with the help of Gateway and Raspberry Pi will 
control various devices attached to it wirelessly or wired. When a 
button is pressed in Fetchit, corresponding device attached to Raspberry 
PI will be triggered based on the device configuration Raspberry Pi 
supports. 

Raspberry Pi:

      Raspberry Pi device acts as a CoAP server/client with DTLS. The 
CoAP server running will get the request from Fetchit and forward to 
Fetchitgo node available in node red community. 

WiFi Router or Ethernet Switch 
	
	The router acts as DHCP server to assign IP address to Raspberry 
Pi and Gateway. It forms a local network so that FetchitGo can control 
any devices connected to Raspberry Pi 

FetchitGo Node:

      There are two nodes in FetchItGO. One is FetchItGO mqtt IN anf FetchItGO mqtt OUT.
      The CoAP server will publish the information about the button pressed in fetchitgo device. 
The published information can be recived in node red using FetchItGO mqtt IN node. The information can be republished again in node red using FetchItGO mqtt OUT node.
So that the Other Raspberry pi on the same network can use for homw automation based on the button you pressed.

For example: Button 1 can be configured for Switch on the light.
             Button 2 can be configured for switch on your cofee machine.

Californium CoAP Source code:

      A CoAP server is instantiated in Raspberry Pi to get requests and 
send response to Fetchitgo device. Californium code is used for this 
purpose. Please download it from here https://github.com/eclipse/californium 

Installation:
      $ sudo npm install node-red-contrib-fetchitgo
