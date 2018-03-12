#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags constants."""

MAJOR_VERSION = 0
MINOR_VERSION = 2
PATCH_VERSION = 0

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

HEADERS = {"content-type": "application/json; charset=utf-8"}
BASEURL = "https://www.mytaglist.com"

SIGN_IN_URL = BASEURL + "/ethAccount.asmx/SignInEx"
IS_SIGNED_IN_URL = BASEURL + "/ethAccount.asmx/IsSignedInEx"
GET_TAGS_URL = BASEURL + "/ethClient.asmx/GetTagList"

ARM_MOTION_URL = BASEURL + "/ethClient.asmx/Arm"
ARM_HUMIDITY_URL = BASEURL + "/ethClient.asmx/ArmCapSensor"
ARM_TEMPERATURE_URL = BASEURL + "/ethClient.asmx/ArmTempSensor"
ARM_LIGHT_URL = BASEURL + "/ethClient.asmx/ArmLightSensor"

DISARM_MOTION_URL = BASEURL + "/ethClient.asmx/DisArm"
DISARM_HUMIDITY_URL = BASEURL + "/ethClient.asmx/DisarmCapSensor"
DISARM_TEMPERATURE_URL = BASEURL + "/ethClient.asmx/DisarmTempSensor"
DISARM_LIGHT_URL = BASEURL + "/ethClient.asmx/DisarmLightSensor"
