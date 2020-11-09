#!/usr/bin/python
import random
import time
import json
import requests
import sys
import paho.mqtt.client as mqtt  
import binascii
import base64
import os 
import struct
from development.loraPayloadDecoder import loraPayloadDecoder
class LoraPayloadProcess:

    ##ip = sys.argv[1]
    ## class variables
    ip = "198.162.1.155"
    macAddress = None
    evb_info = None
    evb_sensors = {}
    msgtopic = None
    isConnected = False
    msgeui = None
    Lora_user = None ##os.environ["lora_username"]
    Lp = loraPayloadDecoder()

    remote_server = "quickstart.messaging.internetofthings.ibmcloud.com"
    clientid= "a:quickstart:MTCDT-20958341"
    lora_client = mqtt.Client()
    remote_client = mqtt.Client(client_id=clientid)

    def setmacAddress(self):
        ##logs in to condiuit and retrieves mac address
        ##response = requests.get('https://127.0.0.1/api/login', params=payload, verify=False)
        ##res = response.json()
        ##token = res["result"]["token"]
        r= requests.get('https://127.0.0.1/api/system', verify=False)
        mac = r.json()
        macAddress = mac["result"]["macAddress"]
        self.macAddress = macAddress.replace(":", "-")
        self.Lora_user = "MTCDT-"+ mac["result"]["deviceId"]
        self.msgtopic = "iot-2/type/mosquitto/id/" + self.macAddress + "/evt/datapoint/" + "fmt/json"
        self.clientid = "a:quickstart:" + self.Lora_user
       ## print(self.clientid + " and " + self.msgtopic)
  #connect lora client to localhost
    def setLoraClient(self):
      self.lora_client.connect("127.0.0.1")
      self.remote_client.connect(self.remote_server, port=1883)
  #callback function initiated on on_connect property for lora client
    def loraOnConnect(self, client, userdata, flags, rc):
      print("Lora Client Connection: " + str(rc)) 	#Returns a 0
      self.lora_client.subscribe("lora/+/up", qos=0)
      self.isConnected = True

    def remoteOnConnect(self, client, userdata, flags, rc):
      print("Remote Client Connection: " + str(rc)) 	#Returns a 0

    def onDisconnect(self, client, userdata, rc):
      self.isConnected = False
      print("The connection has failed.")

    def postXdotData(self, msg):
        msgObj = json.loads(msg)
        msg_payload ={
          "d": {
            "light": msgObj["evb"]["light"]["lux"],
            "moisture": msgObj["evb"]["barometer"]["pa"],
            "temperature": msgObj["evb"]["temperature"]["c"],
            "x_acc": msgObj["evb"]["accelerometer"]["x"],
            "y_acc": msgObj["evb"]["accelerometer"]["y"],
            "z_acc": msgObj["evb"]["accelerometer"]["z"]
          }
        }
        self.evb_info[self.msgeui]["msg_counter"] = None
        if(self.evb_info[self.msgeui]["msg_counter"] == None):
            self.evb_info[self.msgeui]["msg_counter"] = 0
        
        self.evb_info[self.msgeui]["msg_counter"] += 1.0
        return json.dumps(msg_payload)
    def createSimulatedData(self):
        msg = {}
        msg["evb"] = {}
        msg["evb"]["light"] = {}
        msg["evb"]["light"]["lux"] = random.randint(2, 8)
        msg["evb"]["barometer"]= {}
        msg["evb"]["barometer"]["pa"] = 90*random.randint(0, 1)*12
        msg["evb"]["temperature"] = {}
        msg["evb"]["temperature"]["c"] = 20*random.randint(0, 1)*12
        msg["evb"]["accelerometer"] = {}
        msg["evb"]["accelerometer"]["x"] = random.randint(0, 1)
        msg["evb"]["accelerometer"]["y"] = random.randint(0, 1)
        msg["evb"]["accelerometer"]["z"] = random.randint(0, 1)
        msg = json.dumps(msg)
        
        if(self.evb_info == None):
          self.evb_info = {}
          self.evb_info[self.msgeui] = {}
        if (self.evb_info[self.msgeui] == None):
          self.evb_info[self.msgeui] = {"msg_counter": 0}
        return msg
    def setVals(self):
        self.lora_client.on_connect = self.loraOnConnect
        self.lora_client.on_message = self.onMessage
        self.remote_client.on_disconnect = self.onDisconnect
        self.remote_client.on_connect = self.remoteOnConnect

    def onMessage(self, mqtt_client, userdata, msg):
        newMsg = json.loads(msg.payload)
        data = base64.b64decode(newMsg["data"])
        datahex = binascii.hexlify(data)
        self.msgeui = newMsg["deveui"]
        self.Lp.
       
    def runLoop(self):
        while(True):
          time.sleep(1)
	#Creates event loop and new thread that initializes the paho mqtt loops for both clients
    def startLoop(self):
        #UI thread = terminal interaction
        self.lora_client.loop_start()
        self.remote_client.loop_start()




    