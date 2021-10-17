#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags constants."""

MAJOR_VERSION = 0
MINOR_VERSION = 6
PATCH_VERSION = 1

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

HEADERS = {"content-type": "application/json; charset=utf-8"}
BASEURL = "https://my.wirelesstag.net"

SIGN_IN_URL = BASEURL + "/ethAccount.asmx/SignInEx"
IS_SIGNED_IN_URL = BASEURL + "/ethAccount.asmx/IsSignedInEx"
GET_TAGS_URL = BASEURL + "/ethClient.asmx/GetTagList2"

ARM_MOTION_URL = BASEURL + "/ethClient.asmx/Arm"
ARM_HUMIDITY_URL = BASEURL + "/ethClient.asmx/ArmCapSensor"
ARM_TEMPERATURE_URL = BASEURL + "/ethClient.asmx/ArmTempSensor"
ARM_LIGHT_URL = BASEURL + "/ethClient.asmx/ArmLightSensor"

DISARM_MOTION_URL = BASEURL + "/ethClient.asmx/DisArm"
DISARM_HUMIDITY_URL = BASEURL + "/ethClient.asmx/DisarmCapSensor"
DISARM_TEMPERATURE_URL = BASEURL + "/ethClient.asmx/DisarmTempSensor"
DISARM_LIGHT_URL = BASEURL + "/ethClient.asmx/DisarmLightSensor"

LOAD_EVENT_URL_CONFIG_URL = BASEURL + "/ethClient.asmx/LoadEventURLConfig"
SAVE_EVENT_URL_CONFIG_URL = BASEURL + "/ethClient.asmx/SaveEventURLConfig"

REQUEST_CLOUD_PUSH_UPDATE_URL = BASEURL + "/ethComet.asmx?op=GetNextUpdateForAllManagersOnDB2"
SOAP_CLOUD_PUSH_PAYLOAD = '''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetNextUpdateForAllManagersOnDB2 xmlns="http://mytaglist.com/ethComet"><dbid>2</dbid></GetNextUpdateForAllManagersOnDB2></soap:Body></soap:Envelope>'''
SOAP_CLOUD_PUSH_HEADERS = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "http://mytaglist.com/ethComet/GetNextUpdateForAllManagersOnDB2"}
CLOUD_PUSH_XPATH = ".//{http://mytaglist.com/ethComet}GetNextUpdateForAllManagersOnDB2Result"

SECONDS_BETWEEN_SLEEP = 10  # 10 seconds by default
MAX_SECONDS_SLEEP = 600  # 10 minutes

WIRELESSTAG_TYPE_13BIT = 13
WIRELESSTAG_TYPE_ALSPRO = 26
WIRELESSTAG_TYPE_WATER = 32
# Reed/RH (52)???
# Outdoor Probe/Thermocouple	42
WIRELESSTAG_TYPE_PIR = 72
WIRELESSTAG_TYPE_WEMO_DEVICE = 82

# events
# On means in range, Off means out of rang
EVENT_PRESENCE = 'presence'

# On means motion detected, Off means cear
EVENT_MOTION = 'motion'

# On means open, Off means closed
EVENT_DOOR = 'door'

# On means temperature become too cold, Off means normal
EVENT_COLD = 'cold'

# On means hot, Off means normal
EVENT_HEAT = 'heat'

# On means too dry (humidity), Off means normal
EVENT_DRY = 'dry'

# On means too wet (humidity), Off means normal
EVENT_WET = 'wet'

# On means light detected, Off means no light
EVENT_LIGHT = 'light'

# On means moisture detected (wet), Off means no moisture (dry)
EVENT_MOISTURE = 'moisture'

# On means tag battery is low, Off means normal
EVENT_BATTERY = 'battery'

# supported sensor types
SENSOR_TEMPERATURE = 'temperature'
SENSOR_HUMIDITY = 'humidity'
SENSOR_MOISTURE = 'moisture'
SENSOR_LIGHT = 'light'

# supported actions to monitoring specific metric
ARM_TEMPERATURE = 'temperature'
ARM_HUMIDITY = 'humidity'
ARM_MOTION = 'motion'
ARM_LIGHT = 'light'
ARM_MOISTURE = 'moisture'

# humidity binary event states
# NA(0) or Disarmed (1) or Normal(2) or TooDry(3) or TooHumid(4) or ThresholdPending
HUMIDITY_STATE_NA = 0
HUMIDITY_STATE_DISABLED = 1
HUMIDITY_STATE_NORMAL = 2
HUMIDITY_STATE_TOO_DRY = 3
HUMIDITY_STATE_TOO_WET = 4
HUMIDITY_STATE_THRESHOLD_PENDING = 5

# temperature binary event states
# Disarmed(0) or Normal(1) or TooHigh(2) or TooLow(3) or ThresholdPending(4)
TEMP_STATE_DISABLED = 0
TEMP_STATE_NORMAL = 1
TEMP_STATE_TOO_HIGH = 2
TEMP_STATE_TOO_LOW = 3
TEMP_STATE_THRESHOLD_PENDING = 4

# motion binary event states
# spec = {0: 'Disarmed', 1: 'Armed', 2: 'Moved', 3: 'Opened', 4: 'Closed',
#        5: 'DetectedMovement', 6: 'TimedOut', 7: 'Stabilizing', 8: 'CarriedAway',
#        9: 'InFreeFall'}
MOTION_STATE_DISARMED = 0
MOTION_STATE_ARMED = 1
MOTION_STATE_MOVED = 2
MOTION_STATE_OPENED = 3
MOTION_STATE_CLOSED = 4
MOTION_STATE_MOVEMENT_DETECTED = 5
MOTION_STATE_TIMED_OUT = 6
MOTION_STATE_STABILIZING = 7
MOTION_STATE_IN_FREE_FALL = 8
