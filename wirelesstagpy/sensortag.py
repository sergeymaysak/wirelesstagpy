#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Defines sensor model for wirelesstags platform.

Tags could of different types with different set of active working attributes.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/7/2018
"""

import logging
from datetime import datetime

import wirelesstagpy.utils as UTILS
import wirelesstagpy.constants as CONST
from wirelesstagpy.binaryevent import (
    BinaryEvent,
    BINARY_EVENT_SPECS)
from wirelesstagpy.sensor import Sensor

_LOGGER = logging.getLogger(__name__)


class SensorTag:
    """Model representing single wireless sensor tag."""

    def __init__(self, info, platform, mac=None):
        """Init with dictionary and parent WirelessTagPlatform."""
        self._info = info
        self.uuid = self._info['uuid']
        self.tag_id = self._info['slaveId']
        self.name = self._info['name']
        self.temperature = self._info['temperature']
        self.humidity = self._info['cap']
        self.moisture = self.humidity

        # ambient light - working range: 0.1 lux to 200,000 lux
        self.light = self._info['lux']

        # mac address of tag manager this instance belong to
        self.tag_manager_mac = mac

        # binary events specs - built in lazy fashion
        # key - binary event type, value - instance of BinaryEvent
        self._event_specs = {}

        # spec sensors entities
        # key - sensor type, value - instance of Sensor
        self._sensors_spec = {}

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
    def signal_strength(self):
        """Int with signal strength."""
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
        return self.tag_type == CONST.WIRELESSTAG_TYPE_WATER and self.moisture > 0

    @property
    def is_battery_low(self):
        """Return True if detected low battery level."""
        return self.battery_volts <= self.low_battery_threshold

    @property
    def supported_binary_events_types(self):
        """Return supported by tag binary event types (events with state on or off)."""
        events_map = {
            # 13-bit tag - allows everything but not light and moisture
            CONST.WIRELESSTAG_TYPE_13BIT: [
                CONST.EVENT_PRESENCE, CONST.EVENT_BATTERY,
                CONST.EVENT_MOTION, CONST.EVENT_DOOR,
                CONST.EVENT_COLD, CONST.EVENT_HEAT,
                CONST.EVENT_DRY, CONST.EVENT_WET],

            # Moister/water sensor - temperature and moisture only
            CONST.WIRELESSTAG_TYPE_WATER: [
                CONST.EVENT_PRESENCE, CONST.EVENT_BATTERY,
                CONST.EVENT_COLD, CONST.EVENT_HEAT,
                CONST.EVENT_MOISTURE],

            # ALS Pro: allows everything, but not moisture
            CONST.WIRELESSTAG_TYPE_ALSPRO: [
                CONST.EVENT_PRESENCE, CONST.EVENT_BATTERY,
                CONST.EVENT_MOTION, CONST.EVENT_DOOR,
                CONST.EVENT_COLD, CONST.EVENT_HEAT,
                CONST.EVENT_DRY, CONST.EVENT_WET,
                CONST.EVENT_LIGHT],

            # PIR KumoSensor: specialized on motion, but has
            # temperature and humidity as 13-bit tag
            CONST.WIRELESSTAG_TYPE_PIR: [
                CONST.EVENT_PRESENCE, CONST.EVENT_BATTERY,
                CONST.EVENT_MOTION, CONST.EVENT_DOOR,
                CONST.EVENT_COLD, CONST.EVENT_HEAT,
                CONST.EVENT_DRY, CONST.EVENT_WET
            ],

            # Wemo are power switches.
            CONST.WIRELESSTAG_TYPE_WEMO_DEVICE: [CONST.EVENT_PRESENCE]
        }

        # allow everything if tag type is unknown
        # (i just dont have full catalog of them :))
        tag_type = self.tag_type
        fullset = BINARY_EVENT_SPECS.keys()
        return events_map[tag_type] if tag_type in events_map else fullset

    def event_for_type(self, event_type):
        """Return event model for specified type."""
        if event_type not in self.supported_binary_events_types:
            return None

        if event_type in self._event_specs:
            return self._event_specs[event_type]
        else:
            event = BinaryEvent.make_event(event_type, self)
            self._event_specs[event_type] = event
            return event

    @property
    def allowed_sensor_types(self):
        """Return array of allowed sensor types for tag."""
        all_sensors = [CONST.SENSOR_TEMPERATURE,
                       CONST.SENSOR_HUMIDITY,
                       CONST.SENSOR_LIGHT]
        sensors_per_tag_type = {
            CONST.WIRELESSTAG_TYPE_13BIT: [
                CONST.SENSOR_TEMPERATURE,
                CONST.SENSOR_HUMIDITY],
            CONST.WIRELESSTAG_TYPE_WATER: [
                CONST.SENSOR_TEMPERATURE,
                CONST.SENSOR_MOISTURE],
            CONST.WIRELESSTAG_TYPE_ALSPRO: [
                CONST.SENSOR_TEMPERATURE,
                CONST.SENSOR_HUMIDITY,
                CONST.SENSOR_LIGHT],
            CONST.WIRELESSTAG_TYPE_PIR: [
                CONST.SENSOR_TEMPERATURE,
                CONST.SENSOR_HUMIDITY
            ],
            CONST.WIRELESSTAG_TYPE_WEMO_DEVICE: []
        }

        tag_type = self.tag_type
        return (
            sensors_per_tag_type[tag_type] if tag_type in sensors_per_tag_type
            else all_sensors)

    def sensor_for_type(self, sensor_type):
        """Return sensor for specified type or None if not supported by tag."""
        if sensor_type not in self.allowed_sensor_types:
            return None

        if sensor_type in self._sensors_spec:
            return self._sensors_spec[sensor_type]
        else:
            sensor = Sensor.make_sensor(sensor_type, self)
            self._sensors_spec[sensor_type] = sensor
            return sensor

    @property
    def allowed_monitoring_types(self):
        """Return allowed actions to monitor for tag."""
        all_sensors = [
            CONST.ARM_TEMPERATURE, CONST.ARM_HUMIDITY,
            CONST.ARM_MOTION, CONST.ARM_LIGHT]

        sensors_per_tag_spec = {
            CONST.WIRELESSTAG_TYPE_13BIT: [
                CONST.ARM_TEMPERATURE, CONST.ARM_HUMIDITY, CONST.ARM_MOTION],
            CONST.WIRELESSTAG_TYPE_WATER: [
                CONST.ARM_TEMPERATURE, CONST.ARM_MOISTURE],
            CONST.WIRELESSTAG_TYPE_ALSPRO: [
                CONST.ARM_TEMPERATURE, CONST.ARM_HUMIDITY,
                CONST.ARM_MOTION, CONST.ARM_LIGHT],
            CONST.WIRELESSTAG_TYPE_PIR: [
                CONST.ARM_TEMPERATURE, CONST.ARM_HUMIDITY, CONST.ARM_MOTION
            ],
            CONST.WIRELESSTAG_TYPE_WEMO_DEVICE: []
        }

        tag_type = self.tag_type

        result = (
            sensors_per_tag_spec[tag_type]
            if tag_type in sensors_per_tag_spec else all_sensors)
        _LOGGER.info("Allowed switches: %s tag_type: %s",
                     str(result), tag_type)

        return result

    def __repr__(self):
        """Return string representation of tag."""
        # Water/Moisture Sensor supports water and temperature
        if self.tag_type == CONST.WIRELESSTAG_TYPE_WATER:
            return '{} temp: {} leak: {}'.format(self.name, self.temperature, self.is_leaking)
        # ALS Pro (8bit)
        elif self.tag_type == CONST.WIRELESSTAG_TYPE_ALSPRO:
            return '{} temp: {} humidity: {} lux: {}'.format(self.name, self.temperature, self.humidity, self.light)

        # use 13-bit tag supports temp/motion/humidity as fallback for everything else
        return '{} temp: {} humidity: {}'.format(self.name, self.temperature, self.humidity)
