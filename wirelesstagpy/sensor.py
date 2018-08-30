#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Model class representing sensor of specific type.

Single tag contains multiple number of sensors such as
temperature, motion, moisture, humidity or light.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 8/30/2018
"""

import logging
import weakref
import wirelesstagpy.constants as CONST

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    CONST.SENSOR_TEMPERATURE: {
        'unit': '°C',
        'attr': 'temperature',
        'update_attr': 'temp'
    },
    CONST.SENSOR_HUMIDITY: {
        'unit': '%',
        'attr': 'humidity',
        'update_attr': 'cap'
    },
    CONST.SENSOR_MOISTURE: {
        'unit': '%',
        'attr': 'moisture',
        'update_attr': 'cap'
    },
    CONST.SENSOR_LIGHT: {
        'unit': 'lux',
        'attr': 'light',
        'update_attr': 'lux'
    }
}


class Sensor:
    """Entity representing single sensor."""

    @classmethod
    def make_sensor(cls, sensor_type, tag):
        """Build sensor for type with parent tag."""
        spec = SENSOR_TYPES[sensor_type]
        return cls(sensor_type, spec, tag)

    def __init__(self, sensor_type, spec, tag):
        """Init with spec and parent tag."""
        self.sensor_type = sensor_type
        self.unit = spec['unit']
        self._attr = spec['attr']
        self._update_attr = spec['update_attr']
        self._parent_tag = weakref.ref(tag)

    @property
    def value(self):
        """Return current value of sensor."""
        return getattr(self._parent_tag(), self._attr, False)

    def value_from_update_event(self, event_spec):
        """Decode new value from arrived update event."""
        try:
            return event_spec[self._update_attr]
        except Exception as error:
            _LOGGER.error("Failed to get value from event data: %s - %s",
                          event_spec, error)
            return 0

    def __repr__(self):
        """Return string representation."""
        return '{} value: {} of {}'.format(self.sensor_type, self.value, self.unit)
