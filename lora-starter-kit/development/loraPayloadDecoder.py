#!/usr/bin/python
from collections import OrderedDict


class LoraPayload():

	payLoadFormat = OrderedDict()
	numBytesPayload= 0
	payloadData = None

	def __init__(self, format = None):
		if not format == None:	
			if isinstance(ele, dict):
				payLoadFormat = format
	def setPayloadFormat(self):
		self.addItem("0e", "accelerometer", 3)
		self.addItem("08", "barometer", 3)
		self.addItem("05", "lux", 2)
		self.addItem("0b", "temperature", 2)
		
		

	def addItem(self, ID, MEANING, NUMBYTES):
		self.payLoadFormat[MEANING] = {'numBytes' : NUMBYTES, 'ID' : ID , 'startFrom' : self.numBytesPayload}
		self.numBytesPayload = self.numBytesPayload + NUMBYTES + 1

	def setPayload(self, p):
			self.payLoadData = p
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
		
		return json.dumps(msgpayload)

