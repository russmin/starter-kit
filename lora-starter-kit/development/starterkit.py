import random
import json

""" msg.evb={};
msg.evb.light={};
msg.evb.light.lux=Math.random()*8 + 2;
msg.evb.barometer={};
msg.evb.barometer.pa=90*Math.random()*12;
msg.evb.temperature={};
msg.evb.temperature.c=20*Math.random()*12;
msg.evb.accelerometer={};
msg.evb.accelerometer.x=Math.random();
msg.evb.accelerometer.y=Math.random();
msg.evb.accelerometer.z=Math.random();


if (context.global.evb_info == null){
    context.global.evb_info = {};
}

if (context.global.evb_info[msg.eui] == null){
    context.global.evb_info[msg.eui]={ "msg_counter":0 };
}


return msg; """

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

json.dumps(msg)
print(msg)






""" if ( context.global.evb_info[msg.eui] == null) {
  context.global.evb_info[msg.eui] = { msg_counter: 0 };
  
}

var evb_info = context.global.evb_info ;
var evb_sensors = {};

/*
 * Evaluation board properties.
 */
var EVB_TYPE = {
  none: 0,
  led_1: 1,
  led_2: 2,
  lux_max: 3,
  lux_min: 4,
  lux: 5,
  barometer_max: 6,
  barometer_min: 7,
  barometer: 8,
  temperature_max: 9,
  temperature__min: 10,
  temperature: 11,
  accelerometer_max: 12,
  accelerometer_min: 13,
  accelerometer: 14,
  tx_interval: 15,
  amps_max: 16,
  amps_min: 17,
  amps: 18,
  m2x_device: 19,
  m2x_key: 20,
};

/*
 * Process the EVB LoRa payload.
 *
 * EVB payload contains one or more TLV fields.
 *
 * [<type: accelerometer><length: 6><x-high><x-low><y-high><y-low><z-high><z-low>]
 * [<type: barometer><length: 3><byte2><byte1><byte0>]
 * [<type: temperature><length: 2><byte-high><byte-low>]
 * 
 */
for (var index = 0; index < msg.payload.length; ) {
  var type = msg.payload[index++];
//   var length = msg.payload[index++];
  var value;
  console.log("type: " + type + " length: " );

  switch (type) {
  case EVB_TYPE.lux:
    if (typeof(evb_sensors.light) == "undefined") {
      evb_sensors.light = {};
    }

    value = msg.payload[index++] << 8;
    value |= msg.payload[index++];
    value = value * 0.24;

    evb_sensors.light.lux = value;
    break;
  case EVB_TYPE.barometer:
    if (typeof(evb_sensors.barometer) == "undefined") {
      evb_sensors.barometer = {};
    }

    value = msg.payload[index++] << 16;
    value |= msg.payload[index++] << 8;
    value |= msg.payload[index++];
    value = value * 0.00025;

    evb_sensors.barometer.pa = value;
    break;
  case EVB_TYPE.accelerometer:
    if (typeof(evb_sensors.accelerometer) == "undefined") {
      evb_sensors.accelerometer = {};
    }
    // evb_sensors.accelerometer.x = (msg.payload[index++] << 24) >> 16;
    var x1 = evb_sensors.accelerometer.x = msg.payload[index++] ;
    // x1 = ~x1 ; 
    // x1 = ( x1 + 1 ) % 256; 
    evb_sensors.accelerometer.x = x1 * 0.0625//; / 15;
    // evb_sensors.accelerometer.y = (msg.payload[index++] << 24) >> 16;
    var y1 = evb_sensors.accelerometer.y = msg.payload[index++] ;
    // y1 = ~ y1 ; 
    // y1 = ( y1 + 1 ) % 256;
    
    var y1 = evb_sensors.accelerometer.y = y1 * 0.0625 ; // / 15 ;

    // evb_sensors.accelerometer.z = (msg.payload[index++] << 24) >> 16;
    var z1 = evb_sensors.accelerometer.z = msg.payload[index++] ;
    // z1 = ~ z1 ; 
    // z1 = ( z1 + 1 ) % 256; 
    // z1 = z1 - 128;
    var z1 = evb_sensors.accelerometer.z = z1 * 0.0625; // / 15;
    break;
  case EVB_TYPE.temperature:
    if (typeof(evb_sensors.temperature) == "undefined") {
      evb_sensors.temperature = {};
    }

    value = (msg.payload[index++] << 24) >> 16;
    value |= msg.payload[index++];
    value = value * 0.0625;

    evb_sensors.temperature.c = value;
    break;
  case EVB_TYPE.tx_interval:
    evb_sensors.tx_timer = msg.payload[index++];
    break;
  case EVB_TYPE.m2x_device:
    value = msg.payload.slice(index, index + length);
    evb_info[msg.eui].m2x_device = "";
    for (var j = 0; j < length; j++) {
      evb_info[msg.eui].m2x_device += String.fromCharCode(value[j]);
    }
    break;
  case EVB_TYPE.m2x_key:
    value = msg.payload.slice(index, index + length);
    evb_info[msg.eui].m2x_key = "";
    for (var j = 0; j < length; j++) {
      evb_info[msg.eui].m2x_key += String.fromCharCode(value[j]);
    }
    break;
  default:
    index += length;
    break;
  }
}

if (typeof(evb_info[msg.eui].m2x_device) == "undefined") {
  console.log("No m2x_device registered for " + msg.eui);
//   return null;
}
if (typeof(evb_info[msg.eui].m2x_key) == "undefined") {
  console.log("No m2x_key registered for " + msg.eui);
//   return null;
}
msg.m2x_device = evb_info[msg.eui].m2x_device;
msg.m2x_key = evb_info[msg.eui].m2x_key;
msg.evb = evb_sensors;

/*
 * Return msg to continue the flow
 */
if (typeof msg.evb != "undefined"){
  return msg;     
}
 """
