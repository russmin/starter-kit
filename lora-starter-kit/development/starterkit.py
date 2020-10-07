import random
import json
import requests


response = requests.get(http://localhost/api/login?username=admin&password=MTCDT-20958341)
res = response.json()
token = res["token"]
r= requests.get(http://localhost/api/system)
mac = r.json()
macAddress = mac["macAddress"]
maAddress = macAddress.replace(":", "-")
evb_info = {}
evb_sensors = {}


def createSimulatedData(self):
  {
    msg = {}
    msg["evb"] = {}
    msg["evb"]["light"] = {}
    msg["evb"]["light"]["lux"] = random.randint(2, 8)
    msg["evb"]["barometer"]= {}
    msg["evb"]["barometer"]["pa"] = 90*random.randint(0, 1)*12
    msg["evb"]["temperature"] = {}
    msg["evb"]["temperature"]["c"] = 20*random.randint(0, 1)*12
    msg["evb"]["accelerometer"] = {}
    msg["evb"]["accelerometer"]["x"] = random.random(0, 1)
    msg["evb"]["accelerometer"]["y"] = random.random(0, 1)
    msg["evb"]["accelerometer"]["z"] = random.random(0, 1)
    meg = json.dumps(msg)
    return msg; 
  }






Class Switcher(object)
  EVB_TYPE = {
  "none" =  0
  "led_1" = 1
  "led_2" = 2
  "lux_max" = 3
  "lux_min" = 4
  "lux" = 5
  "barometer_max" = 6
  "barometer_min" = 7
  "barometer" = 8
  "temperature_max" = 9
  "temperature_min" = 10
  "temperature" = 11
  "accelerometer_max" = 12
  "accelerometer_min" = 13
  "accelerometer" = 14
  "tx_interval" = 15
  "amps_max" = 16
  "amps_min" = 17
  "amps" =  18
  "m2x_device" = 19
  "m2x_key" = 20
    }
  for (index = 0; index > msg.payload.length)
    {
      type = msg.payload[index++]
      value = None
      print("type: " + type + "length ")

    }
  def switcher(type):
    {
      switcher = {
        0: "EVB_TYPE_lux"
        1: "EVB_TYPE_barometer"
        2: "EVB_TYPE_accelerometer"
        3: "EVB_TYPE_temperature"
        4: "EVB_TYPE_tx_interval"
        5: "EVB_TYPE_m2x_device"
        6: "EVB_TYPE.m2x_key"
      }
    }
  def EVB_TYPE_lux(self, type, msg):
    {
      if (type(evb_sensors["light"]) == None) {
        evb_sensors["light"] = {}
      }

      value = msg["payload"][index++] << 8
      value |= msg["payload"][index++]
      value = value * 0.24

      evb_sensors["light"]["lux"] = value
    }
  def EVB_TYPE_barometer(self, type, msg):
    {
      if (type(evb_sensors["barometer"]) == None) {
        evb_sensors["barometer"] = {}
      }
      value = msg.payload[index++] << 16
      value |= msg.payload[index++] << 8
      value |= msg.payload[index++]
      value = value * 0.00025

      evb_sensors.barometer.pa = value;
    }
  def EVB_TYPE_accelerometer(self, type, msg):
    {
      if (type(evb_sensors["accelerometer"]) == None) {
      evb_sensors["accelerometer"] = {}
    }
    
    var x1 = evb_sensors["accelerometer"]["x"] = msg.payload[index++] 
    ## x1 = ~x1 ; 
    ## x1 = ( x1 + 1 ) % 256; 
    evb_sensors["accelerometer"]["x"] = x1 * 0.0625
    ## evb_sensors.accelerometer.y = (msg.payload[index++] << 24) >> 16;
    var y1 = evb_sensors["accelerometer"]["y"] = msg.payload[index++] 
    ## y1 = ~ y1 ; 
    ## y1 = ( y1 + 1 ) % 256;
    
    var y1 = evb_sensors["accelerometer"]["y"] = y1 * 0.0625   

    ## evb_sensors.accelerometer.z = (msg.payload[index++] << 24) >> 16;
    var z1 = evb_sensors["accelerometer"]["z"] = msg.payload[index++] 
    ## z1 = ~ z1 ; 
    ## z1 = ( z1 + 1 ) % 256; 
    ## z1 = z1 - 128;
    var z1 = evb_sensors["accelerometer"]["z"] = z1 * 0.0625
    }
  def EVB_TYPE_temperature(self, type, msg)
    {
      if (typeof(evb_sensors["temperature"]) == None) {
        evb_sensors["temperature"] = {}
      }

      value = (msg.payload[index++] << 24) >> 16
      value |= msg.payload[index++]
      value = value * 0.0625

      evb_sensors["temperature"]["c"] = value
    }
  def EVB_TYPE_tx_interval(self, type, msg):
    {
      evb_sensors["tx_timer"] = msg.payload[index++]
    }
  def EVB_TYPE_m2x_device(self, type, msg):
    {
      value = msg.payload.slice(index, index + length)
      evb_info[msg.eui]["m2x_device"] = ""
      for ( j = 0; j < length; j++) {
        evb_info[msg.eui].m2x_device += String.fromCharCode(value[j])
    }
  def EVB_TYPE_m2x_interval(self, type, msg):
    {
      value = msg.payload.slice(index, index + length)
      evb_info[msg.eui]["m2x_key"] = ""
      for (j = 0; j < length; j++) {
        evb_info[msg.eui].m2x_key += String.fromCharCode(value[j])
     }
    }


