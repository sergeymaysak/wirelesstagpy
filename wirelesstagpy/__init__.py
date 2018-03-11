#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple python library for wirelesstags REST API.

See http://wirelesstag.net/apidoc.html for more details.
Current implementation is limited to loading info for all available to
registered user sensor tags.
mytaglist.com account credentials are needed to use this lib.
Enabling tags sharing is not required.

"Wireless Sensor Tags", "KumoSensor" and "Kumostat" are trademarks of Cao Gadgets LLC,
see www.wirelesstag.net for more information.
I am in no way affiliated with Cao Gadgets LLC.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/7/2018.
"""

import json
import time
from datetime import datetime
import logging
import requests

from wirelesstagpy.sensortag import SensorTag
from wirelesstagpy.exceptions import WirelessTagsException
import wirelesstagpy.constants as CONST

_LOGGER = logging.getLogger(__name__)


class WirelessTags:
    """Principal class for Wireless Sensors Tags."""

    _HEADERS = CONST.HEADERS
    _SIGN_IN_URL = CONST.SIGN_IN_URL
    _IS_SIGNED_IN_URL = CONST.IS_SIGNED_IN_URL
    _GET_TAGS_URL = CONST.GET_TAGS_URL

    def __init__(self, username, password):
        """Initialize wirelesstags platform."""
        self._username = username
        self._password = password
        self._cookies = None
        self._tags = {}

        # time interval from last reload
        self._last_load_time = 0

        # in seconds
        self._postback_interval = 600

        self.use_celsius = True

        # server time in utc (filetime format)
        self._server_time = 0

    def load_tags(self):
        """Load all registered tags."""
        if self._needs_reload:
            cookies = self._auth_cookies
            try:
                response = requests.post(self._GET_TAGS_URL, headers=self._HEADERS, cookies=cookies)

                # remember time of load for cache/reload management
                self._last_load_time = time.time()

                json_tags_spec = response.json()
                tags = json_tags_spec['d']
                for tag in tags:
                    uuid = tag['uuid']
                    self._tags[uuid] = SensorTag(tag, self)
                _LOGGER.info("tags reloaded at: %s", datetime.now())
            except Exception as error:
                _LOGGER.error("failed to load tags - %s", error)

        return self._tags

    def _login(self):
        """Perform user login."""
        auth = json.dumps({"email": self._username, "password": self._password})
        try:
            response = requests.post(self._SIGN_IN_URL, headers=self._HEADERS, data=auth)
            json_response = response.json()

            self._update_server_settings(json_response['d'])
            self._cookies = response.cookies
        except Exception as error:
            _LOGGER.debug("Failed to login to %s - %s", CONST.BASEURL, error)
            self._cookies = None
            raise WirelessTagsException('Unable to login to wirelesstags.net - check your credentials')

        _LOGGER.info("Login successful")

        return self._cookies

    def _update_server_settings(self, server_info):
        self._postback_interval = server_info['postbackInterval']
        self._server_time = server_info['serverTime']
        self.use_celsius = (server_info['temp_unit'] == 0)

    @property
    def _is_signed_in(self):
        cookies = self._cookies
        result = False
        if cookies is None:
            cookies = self._login()
        try:
            response = requests.post(self._IS_SIGNED_IN_URL, headers=self._HEADERS, cookies=cookies)
            json_response = response.json()
            if 'd' in json_response:
                self._update_server_settings(json_response['d'])
                result = True
        except Exception as error:
            _LOGGER.debug("Failed to check signin status - %s", error)
            self._cookies = None
        return result

    @property
    def _auth_cookies(self):
        if self._is_signed_in:
            return self._cookies

        return self._login()

    @property
    def _needs_reload(self):
        elapsed = time.time() - self._last_load_time
        return elapsed > self._postback_interval

    def __str__(self):
        """Return string representation of wirelesstags platform."""
        temperature_str = 'celsius' if self.use_celsius else 'fahrenheit'
        return 'WirelessTagsPlatform: using {}, update interval: {} server time: {} tags: {}'\
            .format(temperature_str, self._postback_interval, self._server_time, self._tags)
