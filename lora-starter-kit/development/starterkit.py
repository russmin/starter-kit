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

    remote_server = "quickstart.messaging.internetofthings.ibmcloud.com"
    clientid= "a:quickstart:MTCDT-20958341"
    lora_client = mqtt.Client()
    remote_client = mqtt.Client(client_id=clientid)

    def setmacAddress(self):
        ##logs in to condiuit and retrieves mac address
        payload = {'username': 'admin', 'password': 'MTCDT-20958341'}
        response = requests.get('https://192.168.1.155/api/login', params=payload, verify=False)
        res = response.json()
        token = res["result"]["token"]
        r= requests.get('https://192.168.1.155/api/system?token='+ token, verify=False)
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
        self.msgeui = newMsg["deveui"]

        ##data=self.postXdotData(self.createSimulatedData())
        print(msg.payload)
        ##self.remote_client.publish(self.msgtopic, payload=data, qos=0)
        {"tmst":4293983404,"chan":1,"rfch":0,"freq":868.3,"stat":1,"modu":"LORA","datr":"SF12BW125","codr":"4/5","lsnr":10.2,"rssi":-27,"opts":"","size":14,"fcnt":13,"cls":0,"port":1,"mhdr":"40b6feb000000d00","data":"Dv8AEAgGA1oFACsLAW0=","appeui":"7d-75-27-ad-d1-d2-f7-08","deveui":"00-80-00-00-00-01-91-90","ack":false,"adr":false,"gweui":"00-80-00-00-a0-00-63-c3","seqn":13,"time":"2020-10-27T11:09:21.889716Z"}
    def runLoop(self):
		while(True):
			time.sleep(1)

	#Creates event loop and new thread that initializes the paho mqtt loops for both clients
    def startLoop(self):
      #UI thread = terminal interaction
      self.lora_client.loop_start()
      self.remote_client.loop_start()

""" class Switcher:
    EVB_TYPE = {
    "none" : 0,
    "led_1" : 1,
    "led_2" : 2,
    "lux_max" : 3,
    "lux_min" : 4,
    "lux" : 5,
    "barometer_max" : 6,
    "barometer_min" : 7,
    "barometer" : 8,
    "temerature_max" : 9,
    "temperature_min" : 10,
    "temperature" : 11,
    "accelerometer_max" : 12,
    "accelerometer_min" : 13,
    "accelerometer" : 14,
    "tx_interval" : 15,
    "amps_max" : 16,
    "amps_min" : 17,
    "amps" :  18,
    "m2x_device" : 19,
    "m2x_key" : 20
      }
    for (index = 0; index > msg.payload.length; index++)
        {
          type = msg.payload[index]
          length = msg.payload[index]
          value = None
          print("type: " + type + "length ")
        }
    def switcher(type):
        switcher = {
          0: "EVB_TYPE_lux"
          1: "EVB_TYPE_barometer"
          2: "EVB_TYPE_accelerometer"
          3: "EVB_TYPE_temperature"
          4: "EVB_TYPE_tx_interval"
          5: "EVB_TYPE_m2x_device"
          6: "EVB_TYPE.m2x_key"
        }
        return switcher.get(type, "invalid type")

    def EVB_TYPE_lux(self, type, msg):
        if (type(evb_sensors["light"]) == None) {
          evb_sensors["light"] = {}
        }

        value = msg.payload[index++] << 8
        value |= msg.payload[index++]
        value = value * 0.24

        evb_sensors["light"]["lux"] = value

    def EVB_TYPE_barometer(self, type, msg):
        if (type(evb_sensors["barometer"]) == None) {
          evb_sensors["barometer"] = {}
        }
        value = msg.payload[index++] << 16
        value |= msg.payload[index++] << 8
        value |= msg.payload[index++]
        value = value * 0.00025

        evb_sensors.barometer.pa = value;
    def EVB_TYPE_accelerometer(self, type, msg):
        if (type(evb_sensors["accelerometer"]) == None) {
          evb_sensors["accelerometer"] = {}
        }
        
        evb_sensors["accelerometer"]["x"] = msg.payload[index++] 
        ## x1 = ~x1 ; 
        ## x1 = ( x1 + 1 ) % 256; 
        evb_sensors["accelerometer"]["x"] = x1 * 0.0625
        ## evb_sensors.accelerometer.y = (msg.payload[index++] << 24) >> 16;
        evb_sensors["accelerometer"]["y"] = msg.payload[index++] 
        ## y1 = ~ y1 ; 
        ## y1 = ( y1 + 1 ) % 256;
        
        evb_sensors["accelerometer"]["y"] = y1 * 0.0625   

        ## evb_sensors.accelerometer.z = (msg.payload[index++] << 24) >> 16;
        var z1 = evb_sensors["accelerometer"]["z"] = msg.payload[index++] 
        ## z1 = ~ z1 ; 
        ## z1 = ( z1 + 1 ) % 256; 
        ## z1 = z1 - 128;
        var z1 = evb_sensors["accelerometer"]["z"] = z1 * 0.0625

    def EVB_TYPE_temperature(self, type, msg)
        if (typeof(evb_sensors["temperature"]) == None) {
          evb_sensors["temperature"] = {}
        }

        value = (msg.payload[index++] << 24) >> 16
        value |= msg.payload[index++]
        value = value * 0.0625

        evb_sensors["temperature"]["c"] = value

    def EVB_TYPE_tx_interval(self, type, msg):
        evb_sensors["tx_timer"] = msg.payload[index++]

    def EVB_TYPE_m2x_device(self, type, msg):
        value = msg.payload.slice(index, index + length)

        evb_info[msg.eui]["m2x_device"] = ""
        for ( j = 0; j < length; j++) {
          evb_info[msg["eui"]]["m2x_device"] += String.fromCharCode(value[j])
        }

    def EVB_TYPE_m2x_interval(self, type, msg):
        value = msg.payload.slice(index, index + length)
        evb_info[msg["eui"]]["m2x_key"] = ""
        for (j = 0; j < length; j++) {
          evb_info["msg.eui"]["m2x_key"] += String.fromCharCode(value[j])
      }
    def EVB_TYPE.m2x.key(self, type, msg):
        value = msg.payload.slice(index, index + length)
      evb_info[msg.eui].m2x_key = ""
      for (var j = 0; j < length; j++) {
        evb_info[msg.eui].m2x_key += String.fromCharCode(value[j])
      } """
    
def main():
    remoteconnect = LoraPayloadProcess()
    remoteconnect.setmacAddress()
    remoteconnect.startLoop()
    remoteconnect.setVals()
    remoteconnect.setLoraClient()
    remoteconnect.runLoop()

if __name__ == "__main__":
    main()


    