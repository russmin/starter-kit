#!/usr/bin/python
import random
from collections import OrderedDict
import time
import json
import requests
import sys
import paho.mqtt.client as mqtt  
import binascii
import base64
import os 

#3 class to decode lora payload data in hex form
class LoraPayload():

	payLoadFormat = OrderedDict()
	numBytesPayload= 0
	payloadData = None

## sets the payload format fields in the order of the payload
## added for Lora-Packet Mode
	def setPayloadFormat(self):
		self.addItem("0e", "accelerometer", 3)
		self.addItem("08", "barometer", 3)
		self.addItem("05", "lux", 2)
		self.addItem("0b", "temperature", 2)
		
		
## function to add individual packet payload fields
	def addItem(self, ID, MEANING, NUMBYTES):
		self.payLoadFormat[MEANING] = {'numBytes' : NUMBYTES, 'ID' : ID , 'startFrom' : self.numBytesPayload}
		self.numBytesPayload = self.numBytesPayload + NUMBYTES + 1
## sets the local payload variable
	def setPayload(self, p):
			self.payLoadData = p
## function to decode values in array for the payload
	def getPayload(self):
		if not self.payLoadData == None:
			dataArray = {}
			for (key, value) in self.payLoadFormat.items():
					dataArray[key] = self.getValue(key)
			return dataArray
	def getValue(self, meaning):
		if meaning in self.payLoadFormat:
			s = self.payLoadFormat[meaning]['startFrom'] * 2 + 2
			e = s + self.payLoadFormat[meaning]['numBytes'] * 2 
			data = self.payLoadData[s:e]
			if (meaning == "lux"):
				data = int(data, 16)
				return data * 0.24
			if (meaning == "barometer"):
				data = int(data, 16)
				return data * 0.00025
			if (meaning == "accelerometer"):
				x1 = int(data[0:1], 16) * 0.0625
				y1 = int(data[2:3], 16) * 0.0625 
				z1 = int(data[4:5], 16) * 0.0625 
				acc = {'x1': x1,'y1': y1,'z1': z1}
				return acc
			if (meaning == "temperature"):
				data = int(data, 16)
				return data * 0.0625
	def printFormat(self):
		output = ""
		output += "| LoraPacket payload format"
		output += "| meaning | number of bytes | type | startposition"
		for (key, value) in self.payLoadFormat.items():
			output += "| {} : {} : {} : {}".format(key, str(value['numBytes']), str(value['startFrom']))
		return output

#function to return payload into a json format to be sent
	def printValues(self):
		payload = self.getPayload()
		msgpayload =  { 
			"d": {
			"light": payload["lux"],
			"moisture": payload["barometer"],
			"temperature": payload["temperature"],
			"x_acc": payload["accelerometer"]["x1"],
			"y_acc": payload["accelerometer"]["y1"],
			"z_acc": payload["accelerometer"]["z1"]
			}
		}
		
		return json.dumps(msgpayload, sort_keys=True)

		## class for connected to Lora network and remote Mqtt client
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
		Lp = None

		remote_server = "quickstart.messaging.internetofthings.ibmcloud.com"
		clientid= "a:quickstart:MTCDT-20958341"
		lora_client = mqtt.Client()
		remote_client = mqtt.Client(client_id=clientid)

		def setmacAddress(self):
				##logs in to condiuit and retrieves mac address
				r= requests.get('https://127.0.0.1/api/system', verify=False)
				mac = r.json()
				macAddress = mac["result"]["macAddress"]
				self.macAddress = macAddress.replace(":", "-")
			##	self.Lora_user = "MTCDT-"+ mac["result"]["deviceId"]
				self.msgtopic = "iot-2/type/mosquitto/id/" + self.macAddress + "/evt/datapoint/" + "fmt/json"
				##self.clientid = "a:quickstart:" + self.Lora_user
			 	##print(self.clientid + " and " + self.msgtopic)
	#connect lora client to localhost
		def setLoraClient(self):
			self.lora_client.connect("127.0.0.1")
			self.remote_client.connect(self.remote_server, port=1883)
	#callback function initiated on on_connect property for lora client
		def loraOnConnect(self, client, userdata, flags, rc):
			print("Lora Client Connection: " + str(rc)) 	#Returns a 0
			self.lora_client.subscribe("lora/+/up", qos=0)
			self.isConnected = True
	## callback function inititated on_connect poperty on remote client
		def remoteOnConnect(self, client, userdata, flags, rc):
			print("Remote Client Connection: " + str(rc)) 	#Returns a 0
	## callback function inititated on_disconnect poperty on lora client
		def onDisconnect(self, client, userdata, rc):
			self.isConnected = False
			print("The connection has failed.")
	# callback function inititated on_disconnect poperty on remote client
		def remoteOnDisconnect(self, client, userdata, rc):
			print("Remote connection has failed.")

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

		def setVals(self, lp):
				self.lora_client.on_connect = self.loraOnConnect
				self.lora_client.on_message = self.onMessage
				self.lora_client.on_disconnect = self.onDisconnect
				self.remote_client.on_disconnect = self.remoteOnDisconnect
				self.remote_client.on_connect = self.remoteOnConnect
				self.Lp = lp
		def onMessage(self, mqtt_client, userdata, msg):
				newMsg = json.loads(msg.payload)
				data = base64.b64decode(newMsg["data"])
				datahex = binascii.hexlify(data)
				self.msgeui = newMsg["deveui"]
				self.Lp.setPayload(datahex)
				msg = self.Lp.printValues()
				self.remote_client.publish(self.msgtopic, payload=msg, qos=0)
				print(msg)
			 
		def runLoop(self):
				while(True):
					time.sleep(1)
	#Creates event loop and new thread that initializes the paho mqtt loops for both clients
		def startLoop(self):
				#UI thread = terminal interaction
				self.lora_client.loop_start()
				self.remote_client.loop_start()

def main():
	lp = LoraPayload()
	lp.setPayloadFormat()
	instance = LoraPayloadProcess() 
	instance.setmacAddress()
		#create instance of class
	instance.startLoop()
		#need to call setVals first because they wont connect to the call backs if the setClient functions are called first
	instance.setVals(lp) 
					#set connect and message properties & infinite loop
	instance.setLoraClient()
			#connect to local host
	instance.runLoop()

if __name__ == "__main__":
	main()



		