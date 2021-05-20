#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Simple python library for wirelesstags REST API.

See http://wirelesstag.net/apidoc.html for more details.
Current implementation includes:
- loading info for all available to user sensor tags
- manage local push notifications
- arm/disarm tags on monitoring for
humidity, temp, light and motion
mytaglist.com account credentials are needed to use this lib.
Enabling tags sharing is not required.

"Wireless Sensor Tags", "KumoSensor" and "Kumostat" are
trademarks of Cao Gadgets LLC,
see www.wirelesstag.net for more information.
I am in no way affiliated with Cao Gadgets LLC.

Copyrights: (c) 2018-2021 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/7/2018.
"""

import json
import time
from datetime import datetime
import logging
from xml.etree import ElementTree
from threading import Thread
from threading import Lock
import requests

from wirelesstagpy.sensortag import SensorTag
from wirelesstagpy.exceptions import WirelessTagsException
from wirelesstagpy.notificationconfig import NotificationConfig
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

        # array of tag managers mac addresses
        self.mac_addresses = []

        self._is_cloud_push_active = False
        self._update_lock = Lock()
        self._thread = None

    def load_tags(self):
        """Load all registered tags."""
        if self._needs_reload:
            cookies = self._auth_cookies
            try:
                response = requests.post(
                    self._GET_TAGS_URL, headers=self._HEADERS, cookies=cookies)

                # remember time of load for cache/reload management
                self._last_load_time = time.time()

                json_tags_spec = response.json()
                tags = json_tags_spec['d']
                self._update_tags(tags)
                _LOGGER.info("Tags reloaded at: %s", datetime.now())
            except Exception as error:
                _LOGGER.error("failed to load tags - %s", error)

        return self._tags

    def arm_motion(self, tag_id, mac=None):
        """Arm motion sensor to monitor changes."""
        payload = {"id": tag_id, "door_mode_set_closed": True}
        return self._arm_control_tag(tag_id, CONST.ARM_MOTION_URL,
                                     mac, payload)

    def arm_temperature(self, tag_id, mac=None):
        """Arm temperature sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.ARM_TEMPERATURE_URL, mac)

    def arm_humidity(self, tag_id, mac=None):
        """Arm humidity sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.ARM_HUMIDITY_URL, mac)

    def arm_light(self, tag_id, mac=None):
        """Arm light sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.ARM_LIGHT_URL, mac)

    def disarm_motion(self, tag_id, mac=None):
        """Disarm motion sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.DISARM_MOTION_URL, mac)

    def disarm_temperature(self, tag_id, mac=None):
        """Disarm temperature sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.DISARM_TEMPERATURE_URL, mac)

    def disarm_humidity(self, tag_id, mac=None):
        """Disarm humidity sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.DISARM_HUMIDITY_URL, mac)

    def disarm_light(self, tag_id, mac=None):
        """Arm light sensor to monitor changes."""
        return self._arm_control_tag(tag_id, CONST.DISARM_LIGHT_URL, mac)

    def install_push_notification(
            self, tag_id, notifications, apply_to_all=False, tag_manager_mac=None):
        """Install set of push notifications for specified tag."""
        def list_to_spec(array):
            """Sub-func to represent notifications as dictionary."""
            spec = {}
            for item in array:
                spec[item.name] = item.spec
            return spec

        installed_spec = list_to_spec(self.fetch_push_notifications(tag_id))
        requested_spec = list_to_spec(notifications)

        new_config = installed_spec
        for name, _ in installed_spec.items():
            if name in requested_spec:
                new_config[name] = requested_spec[name]

        succeed = True
        cookies = self._auth_cookies
        try:
            payload = {
                "config": new_config,
                "applyAll": apply_to_all,
                "id": tag_id if not apply_to_all else -1
            }
            headers = self._headers_for_mac(tag_manager_mac)
            response = requests.post(CONST.SAVE_EVENT_URL_CONFIG_URL,
                                     headers=headers,
                                     cookies=cookies,
                                     data=json.dumps(payload))
            succeed = "d" in response.json()
        except Exception as error:
            _LOGGER.error("Failed to save notifications config: %s - %s",
                          tag_id, error)
            succeed = False

        return succeed

    def fetch_push_notifications(self, tag_id, tag_manager_mac=None):
        """Read from tags manager current set of push notifications."""
        cookies = self._auth_cookies
        notifications = []
        try:
            payload = json.dumps({"id": tag_id})
            headers = self._headers_for_mac(tag_manager_mac)
            response = requests.post(
                CONST.LOAD_EVENT_URL_CONFIG_URL, headers=headers,
                cookies=cookies, data=payload)
            json_notifications_spec = response.json()
            set_spec = json_notifications_spec['d']
            for name, spec in set_spec.items():
                if "url" in spec:
                    notifications.append(NotificationConfig(name, spec))
        except Exception as error:
            _LOGGER.error("failed to fetch : %s - %s", tag_id, error)
        return notifications

    @property
    def is_monitoring(self):
        """Return if cloud push monitoring is active or not."""
        return self._is_cloud_push_active

    def start_monitoring(self, handler):
        """Start monitoring of state changes with push from cloud."""
        if self._is_cloud_push_active is True:
            return

        self._is_cloud_push_active = True
        self._start_monitoring_thread(handler)

    def stop_monitoring(self):
        """Stop monitoring of state changes from cloud."""
        if self._is_cloud_push_active is False:
            return

        self._is_cloud_push_active = False
        self._thread.join(timeout=1)

    def _start_monitoring_thread(self, handler):
        """Start working thread for monitoring cloud push."""
        def _cloud_push_worker(handler):
            """Worker function for thread."""
            while True:
                if not self._is_cloud_push_active:
                    break
                try:
                    tags_updated = self._request_push_update()
                    if tags_updated is not None and len(tags_updated) > 0:
                        updated_tags, events = self._update_tags(tags_updated)
                        handler(updated_tags, events)
                except Exception as error:
                    _LOGGER.error("failed to get cloud push: %s",
                                  error)

        self._thread = Thread(target=_cloud_push_worker, args=(handler, ))
        self._thread.start()

    def _request_push_update(self):
        """Request push update for tags states."""
        cookies = self._auth_cookies
        tags_updated = []
        try:
            payload = CONST.SOAP_CLOUD_PUSH_PAYLOAD
            headers = CONST.SOAP_CLOUD_PUSH_HEADERS
            response = requests.post(
                CONST.REQUEST_CLOUD_PUSH_UPDATE_URL, headers=headers,
                cookies=cookies, data=payload)
            root = ElementTree.fromstring(response.content)
            raw_tags = root.find(CONST.CLOUD_PUSH_XPATH)
            tags_updated = json.loads(raw_tags.text)
        except Exception as error:
            _LOGGER.error("failed to fetch push update: %s", error)
        return tags_updated

    def _update_tags(self, tags):
        """Update tags arrived from server."""
        updated_tags = {}
        binary_events = {}
        with self._update_lock:
            for tag in tags:
                uuid = tag['uuid']
                # save mac - a unique identifier of specific tag manager
                mac = tag['mac'] if 'mac' in tag else None
                new_tag = SensorTag(tag, self, mac)
                old_tag = self._tags[uuid] if uuid in self._tags else None
                detected_events = new_tag.detected_events(old_tag)
                if detected_events is not None and len(detected_events) > 0:
                    binary_events[uuid] = detected_events
                self._tags[uuid] = new_tag
                self._register_mac(mac)
                updated_tags[uuid] = new_tag
        return (updated_tags, binary_events)

    def _arm_control_tag(self, tag_id, url, tag_manager_mac=None, own_payload=None):
        """Arm sensor with specified id and url to monitor changes."""
        cookies = self._auth_cookies
        sensor_tag = None
        try:
            payload = json.dumps((
                {"id": tag_id} if own_payload is None else own_payload))
            headers = self._headers_for_mac(tag_manager_mac)
            response = requests.post(
                url, headers=headers, cookies=cookies, data=payload)
            json_tags_spec = response.json()
            tag = json_tags_spec['d']
            uuid = tag['uuid']
            self._tags[uuid] = SensorTag(tag, self, tag_manager_mac)
            sensor_tag = self._tags[uuid]
        except Exception as error:
            _LOGGER.error("failed to arm/disarm for tag id: %s - %s",
                          tag_id, error)
        return sensor_tag

    def _headers_for_mac(self, tag_manager_mac):
        """Build headers for http request."""
        headers = self._HEADERS
        # combination of tag_id and X-Set-Mac header with mac
        # allows to uniquely identify tag across multiple tag managers
        if tag_manager_mac is not None:
            headers['X-Set-Mac'] = tag_manager_mac
        return headers

    def _login(self):
        """Perform user login."""
        auth = json.dumps({
            "email": self._username, "password": self._password})
        try:
            response = requests.post(
                self._SIGN_IN_URL, headers=self._HEADERS, data=auth)
            json_response = response.json()

            self._update_server_settings(json_response['d'])
            self._cookies = response.cookies
        except Exception as error:
            _LOGGER.debug("Failed to login to %s - %s", CONST.BASEURL, error)
            self._cookies = None
            raise WirelessTagsException("Unable to login to wirelesstags.net"
                                        " - check your credentials") from error

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
            response = requests.post(
                self._IS_SIGNED_IN_URL, headers=self._HEADERS, cookies=cookies)
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

    def _register_mac(self, mac):
        if mac not in self.mac_addresses:
            self.mac_addresses.append(mac)

    def __str__(self):
        """Return string representation of wirelesstags platform."""
        temperature_str = 'celsius' if self.use_celsius else 'fahrenheit'
        return "WirelessTagsPlatform: using {}," \
               "update interval: {} server time: {} tags: {}"\
               .format(temperature_str, self._postback_interval,
                       self._server_time, self._tags)
