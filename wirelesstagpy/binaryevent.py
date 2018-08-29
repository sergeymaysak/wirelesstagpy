#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Model class event with binary state (on/off) for wirelesstags platform.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 8/20/2018
"""

import weakref
import wirelesstagpy.constants as CONST
import wirelesstagpy.notificationconfig as NS

# Binary event type specification:
# Human Readable Name,
# device_class/type,
# push notification type representing 'on',
# push notification type representing 'of',
# attr to check state
BINARY_EVENT_SPECS = {
    CONST.EVENT_PRESENCE: ['Presence', CONST.EVENT_PRESENCE, 'is_in_range', {
        "on": "oor",
        "off": "back_in_range"
    }, 2],
    CONST.EVENT_MOTION: ['Motion', CONST.EVENT_MOTION, 'is_moved', {
        "on": "motion_detected",
    }, 5],
    CONST.EVENT_DOOR: ['Door', CONST.EVENT_DOOR, 'is_door_open', {
        "on": "door_opened",
        "off": "door_closed"
    }, 5],
    CONST.EVENT_COLD: ['Cold', CONST.EVENT_COLD, 'is_cold', {
        "on": "temp_toolow",
        "off": "temp_normal"
    }, 4],
    CONST.EVENT_HEAT: ['Heat', CONST.EVENT_HEAT, 'is_heat', {
        "on": "temp_toohigh",
        "off": "temp_normal"
    }, 4],
    CONST.EVENT_DRY: ['Too dry', CONST.EVENT_DRY, 'is_too_dry', {
        "on": "too_dry",
        "off": "cap_normal"
    }, 2],
    CONST.EVENT_WET: ['Too wet', CONST.EVENT_WET, 'is_too_humid', {
        "on": "too_humid",
        "off": "cap_normal"
    }, 2],
    CONST.EVENT_LIGHT: ['Light', CONST.EVENT_LIGHT, 'is_light_on', {
        "on": "too_bright",
        "off": "light_normal"
    }, 1],
    CONST.EVENT_MOISTURE: ['Leak', CONST.EVENT_MOISTURE, 'is_leaking', {
        "on": "water_detected",
        "off": "water_dried",
    }, 1],
    CONST.EVENT_BATTERY: ['Low Battery', CONST.EVENT_BATTERY, 'is_battery_low', {
        "on": "low_battery"
    }, 3]
}


class BinaryEvent:
    """Model representing event with binary state."""

    @classmethod
    def make_event(cls, event_type, sensortag):
        """Create event of specific type and tag."""
        spec_list = BINARY_EVENT_SPECS[event_type]
        return cls(spec_list, sensortag)

    def __init__(self, spec_list, sensortag):
        """Init event with attributes list and tag."""
        self.human_readable_name = spec_list[0]
        self.type = spec_list[1]
        self._tag_attr = spec_list[2]
        self.notification_spec = spec_list[3]
        self.tag_id_template = spec_list[4]
        self._parent_tag = weakref.ref(sensortag)

        if (sensortag.tag_type == CONST.WIRELESSTAG_TYPE_PIR and
                self.type == CONST.EVENT_MOTION):
            self.tag_id_template = 2

    def build_notifications(self, url, mac):
        """Construct push notifications for event."""
        configs = []
        for state, name in self.notification_spec.items():
            content = ('{"type": "' + self.type +
                       '", "id":{' + str(self.tag_id_template) +
                       '}, "mac":\"' + mac +
                       '\", "state": \"' + state + '\"}')
            config = NS.NotificationConfig.make_post_local(name, url, content)
            configs.append(config)

        return configs

    @property
    def is_state_on(self):
        """Return binary event state."""
        return getattr(self._parent_tag(), self._tag_attr, False)
