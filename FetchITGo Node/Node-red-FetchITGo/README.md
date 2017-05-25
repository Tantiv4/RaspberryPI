                                                   README
Introduction:
        The document explains the requirement and steps required for handling requests from Fetchitgo device in local network without any internet with the help of Raspberry Pi device.

About Fetchitgo:
          Fetchit will communicate to a CoAP server running in a Raspberry PI device with the help of Gateway and Raspberry Pi will control various devices attached to it wirelessly or wired. When a button is pressed in Fetchit, corresponding device attached to Raspberry PI will be triggered based on the device configuration Raspberry Pi supports. 

Raspberry Pi:
      Raspberry Pi device acts as a CoAP server/client with DTLS. The CoAP server running will get the request from Fetchit and forward to Fetchitgo node available in node red community.
WiFi Router or Ethernet Switch
The router acts as DHCP server to assign IP address to Raspberry Pi and Gateway. It forms a local network so that FetchitGo can control any devices connected to Raspberry Pi

FetchitGo Node:
      A node is created in node red repositories which get the requests from Raspberry Pi and forwards to request device attached. 
     
     The FetchGo-request node will use the GET method to get the requests received by the CoAP-Server which is running in RPi.         This node will return the “msg.payload” in JSON format. 
      E.g: {“aaa”:“bbb”}  
      
      The “msg.payload” format can be modified in CoAP server by user. 

      The FetchGO-mqtt publisher node will publish the received status “msg.payload” to the subscriber node. Here the subscriber node can be a device which is using for home automation. The Subscriber should be connected to the same network. 

Californium CoAP Source code:
      A CoAP server is instantiated in Raspberry Pi to get requests and send response to Fetchitgo device. Californium code is used for this purpose. Please download it from here https://github.com/eclipse/californium

Installation:
      $ sudo npm install node-red-contrib-fetchitgo




