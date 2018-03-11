#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Defines sensor model for wirelesstags platform.

Tags could of different types with different set of active working attributes.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/7/2018
"""

from datetime import datetime
import wirelesstagpy.utils as UTILS


class SensorTag:
    """Model representing single wireless sensor tag."""

    def __init__(self, info, platform):
        """Init with dictionary and parent WirelessTagPlatform."""
        self._info = info
        self._api = platform
        self.uuid = self._info['uuid']
        self.name = self._info['name']
        self.temperature = self._info['temperature']
        self.humidity = self._info['cap']

        # ambient light - working range: 0.1 lux to 200,000 lux
        self.light = self._info['lux']

    @property
    def in_celcius(self):
        """Return temperature's units of measure.

        True for Celcius, False for Fahrenheit.
        """
        return self._api.use_celsius

    @property
    def battery_remaining(self):
        """Return float in percents of remaining battery charge."""
        return self._info['batteryRemaining']

    @property
    def battery_volts(self):
        """Return current voltage of battery as float in volts."""
        return self._info['batteryVolt']

    @property
    def tag_type(self):
        """Int representing tag type.

        Known types are: 1) Regular, 2) 13-bit, 3) Pro, 4) Pro ALS.
        """
        return self._info['tagType']

    @property
    def comment(self):
        """Return comment assigned by end user for this instance."""
        return self._info['comment']

    @property
    def is_alive(self):
        """Bool indicating if hw instance is alive."""
        return self._info['alive']

    @property
    def signal_straight(self):
        """Int with signal straight."""
        return self._info['signaldBm']

    @property
    def beep_option(self):
        """Enum value indicating selected beep option (5, 10, 15 times etc)."""
        return self._info['beepDurationDefault']

    @property
    def is_in_range(self):
        """Is in range (bool).

        Indicates if instance is in range of tags bridge and
        can be accessible for data (as bool).
        """
        return self._info['OutOfRange'] is False

    @property
    def hw_revision(self):
        """Hardware revision - as int."""
        return self._info['rev']

    @property
    def sw_version(self):
        """Software/Firmware revision - as int."""
        return self._info['version1']

    @property
    def power_consumption(self):
        """Power consumption in percents from max possible."""
        level = self._info['txpwr']
        return level * 100.0 / 255.0

    @property
    def last_load_time(self):
        """Datetime in utc. Represents last time when data from sensors was received."""
        communication_time = self._info['lastComm']
        return UTILS.convert_filetime_to_dt(communication_time)

    @property
    def time_since_last_update(self):
        """Time delta since last sensor data load."""
        return datetime.utcnow() - self.last_load_time

    def __str__(self):
        """Return string representation of tag."""
        return '{} temp: {} humidity: {}'.format(self.name, self.temperature, self.humidity)
