#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags constants."""

MAJOR_VERSION = 0
MINOR_VERSION = 1
PATCH_VERSION = 0

__version__ = '{}.{}.{}'.format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

HEADERS = {"content-type": "application/json; charset=utf-8"}
BASEURL = "https://www.mytaglist.com"

SIGN_IN_URL = BASEURL + "/ethAccount.asmx/SignInEx"
IS_SIGNED_IN_URL = BASEURL + "/ethAccount.asmx/IsSignedInEx"
GET_TAGS_URL = BASEURL + "/ethClient.asmx/GetTagList"
