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
        self.tag_id = self._info['slaveId']
        self.name = self._info['name']
        self.temperature = self._info['temperature']
        self.humidity = self._info['cap']
        self.moisture = self.humidity

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
    def low_battery_threshold(self):
        """Return amount of volts triggering low battery notification."""
        return self._info['LBTh']

    @property
    def tag_type(self):
        """Int representing tag type."""
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

    @property
    def motion_state(self):
        """Return state of motion sensor."""
        # spec = {0: 'Disarmed', 1: 'Armed', 2: 'Moved', 3: 'Opened', 4: 'Closed',
        #        5: 'DetectedMovement', 6: 'TimedOut', 7: 'Stabilizing', 8: 'CarriedAway',
        #        9: 'InFreeFall'}
        return self._info['eventState']

    @property
    def is_motion_sensor_armed(self):
        """Return True if tag armed and listens to motion evens."""
        return self.motion_state != 0

    @property
    def humidity_sensor_state(self):
        """Return state of humidity event state."""
        # NA(0) or Disarmed (1) or Normal(2) or TooDry(3) or TooHumid(4) or ThresholdPending
        return self._info['capEventState']

    @property
    def is_humidity_sensor_armed(self):
        """Return True if tag armed and listens to humidity changes events."""
        cap_state = self.humidity_sensor_state
        return cap_state not in [0, 1]

    @property
    def moisture_sensor_state(self):
        """Return moisture state."""
        return self.humidity_sensor_state

    @property
    def is_moisture_sensor_armed(self):
        """Return True if tag armed and listens to moisture level events."""
        return self.is_humidity_sensor_armed

    @property
    def temperature_sensor_state(self):
        """Return state of temp sensor monitoring."""
        # Disarmed(0) or Normal(1) or TooHigh(2) or TooLow(3) or ThresholdPending(4)
        return self._info['tempEventState']

    @property
    def is_temperature_sensor_armed(self):
        """Return True if tag armed and listens to temperature changes evens."""
        return self.temperature_sensor_state != 0

    @property
    def light_sensor_state(self):
        """Return state of light sensor monitoring.

        States: NA (0) or Disarmed(1) or Normal or TooDark or TooBright or ThresholdPending.
        """
        return self._info['lightEventState']

    @property
    def is_light_sensor_armed(self):
        """Return True if tag armed and listens to light changes evens."""
        light_state = self.light_sensor_state
        return light_state not in [0, 1]

    @property
    def is_moved(self):
        """Return True if detected movement."""
        return self.motion_state == 2  # Moved

    @property
    def is_door_open(self):
        """Return True if detected door opening."""
        return self.motion_state == 3  # Open

    @property
    def is_cold(self):
        """Return True if temperature is too low."""
        return self.temperature_sensor_state == 3  # TooLow

    @property
    def is_heat(self):
        """Return True if temperature is too high."""
        return self.temperature_sensor_state == 2  # TooHigh

    @property
    def is_too_dry(self):
        """Return True if humidity is too low (<20%)."""
        return self.humidity_sensor_state == 3  # TooDry

    @property
    def is_too_humid(self):
        """Return True if humidity is too wet (>80%)."""
        return self.humidity_sensor_state == 4  # TooHumid

    @property
    def is_light_on(self):
        """Return True if detected light."""
        return self.light > 0

    @property
    def is_leaking(self):
        """Return True if detected water leak - applicable for water sensor only."""
        return self.tag_type == 32 and self.moisture > 0

    @property
    def is_battery_low(self):
        """Return True if detected low battery level."""
        return self.battery_volts <= self.low_battery_threshold

    def __repr__(self):
        """Return string representation of tag."""
        # Water/Moisture Sensor supports water and temperature
        if self.tag_type == 32:
            return '{} temp: {} leak: {}'.format(self.name, self.temperature, self.is_leaking)
        # ALS Pro (8bit)
        elif self.tag_type == 26:
            return '{} temp: {} humidity: {} lux: {}'.format(self.name, self.temperature, self.humidity, self.light)

        # use 13-bit tag supports temp/motion/humidity as fallback for everything else
        return '{} temp: {} humidity: {}'.format(self.name, self.temperature, self.humidity)
