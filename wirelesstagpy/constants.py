#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags constants."""

MAJOR_VERSION = 0
MINOR_VERSION = 5
PATCH_VERSION = 0

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

REQUEST_CLOUD_PUSH_UPDATE_URL = BASEURL + "/ethComet.asmx?op=GetNextUpdate2"
SOAP_CLOUD_PUSH_PAYLOAD = '''<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetNextUpdate2 xmlns="http://mytaglist.com/ethComet"/></soap:Body></soap:Envelope>'''
SOAP_CLOUD_PUSH_HEADERS = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "http://mytaglist.com/ethComet/GetNextUpdate2"}
CLOUD_PUSH_XPATH = ".//{http://mytaglist.com/ethComet}GetNextUpdate2Result"

WIRELESSTAG_TYPE_13BIT = 13
WIRELESSTAG_TYPE_ALSPRO = 26
WIRELESSTAG_TYPE_WATER = 32
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
