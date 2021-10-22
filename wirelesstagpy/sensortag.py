#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Defines sensor model for wirelesstags platform.

Tags could of different types with different set of active working attributes.

Copyrights: (c) 2018-2021 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/7/2018
"""

import logging
from datetime import datetime

import wirelesstagpy.utils as UTILS
import wirelesstagpy.constants as CONST
from wirelesstagpy.binaryevent import (
    BinaryEvent,
    BinaryEventProxy,
    BINARY_EVENT_SPECS)
from wirelesstagpy.sensor import (
    Sensor,
    SensorProxy)

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
    def motion_state(self) -> int:
        """Return state of motion sensor."""
        # spec = {0: 'Disarmed', 1: 'Armed', 2: 'Moved', 3: 'Opened', 4: 'Closed',
        #        5: 'DetectedMovement', 6: 'TimedOut', 7: 'Stabilizing', 8: 'CarriedAway',
        #        9: 'InFreeFall'}
        return self._info['eventState']

    @property
    def is_motion_sensor_armed(self) -> bool:
        """Return True if tag armed and listens to motion evens."""
        return self.motion_state != CONST.MOTION_STATE_DISARMED

    @property
    def humidity_sensor_state(self) -> int:
        """Return state of humidity event state."""
        # NA(0) or Disarmed (1) or Normal(2) or TooDry(3) or TooHumid(4) or ThresholdPending
        return self._info['capEventState']

    @property
    def is_humidity_sensor_armed(self) -> bool:
        """Return True if tag armed and listens to humidity changes events."""
        cap_state = self.humidity_sensor_state
        return cap_state not in [CONST.HUMIDITY_STATE_NA, CONST.HUMIDITY_STATE_DISABLED]

    @property
    def moisture_sensor_state(self) -> int:
        """Return moisture state."""
        return self.humidity_sensor_state

    @property
    def is_moisture_sensor_armed(self) -> bool:
        """Return True if tag armed and listens to moisture level events."""
        return self.is_humidity_sensor_armed

    @property
    def temperature_sensor_state(self) -> int:
        """Return state of temp sensor monitoring."""
        # Disarmed(0) or Normal(1) or TooHigh(2) or TooLow(3) or ThresholdPending(4)
        return self._info['tempEventState']

    @property
    def is_temperature_sensor_armed(self) -> bool:
        """Return True if tag armed and listens to temperature changes evens."""
        return self.temperature_sensor_state != CONST.TEMP_STATE_DISABLED

    @property
    def light_sensor_state(self) -> int:
        """Return state of light sensor monitoring.

        States: NA (0) or Disarmed(1) or Normal or TooDark or TooBright or ThresholdPending.
        """
        return self._info['lightEventState']

    @property
    def is_light_sensor_armed(self) -> bool:
        """Return True if tag armed and listens to light changes evens."""
        light_state = self.light_sensor_state
        return light_state not in [0, 1]

    @property
    def is_moved(self) -> bool:
        """Return True if detected movement."""
        return self.motion_state == CONST.MOTION_STATE_MOVED  # Moved

    @property
    def is_door_open(self) -> bool:
        """Return True if detected door opening."""
        return self.motion_state == CONST.MOTION_STATE_OPENED  # Open

    @property
    def is_cold(self) -> bool:
        """Return True if temperature is too low."""
        return self.temperature_sensor_state == CONST.TEMP_STATE_TOO_LOW  # TooLow

    @property
    def is_heat(self) -> bool:
        """Return True if temperature is too high."""
        return self.temperature_sensor_state == CONST.TEMP_STATE_TOO_HIGH  # TooHigh

    @property
    def is_too_dry(self) -> bool:
        """Return True if humidity is too low (<20%)."""
        return self.humidity_sensor_state == CONST.HUMIDITY_STATE_TOO_DRY  # TooDry

    @property
    def is_too_humid(self) -> bool:
        """Return True if humidity is too wet (>80%)."""
        return self.humidity_sensor_state == CONST.HUMIDITY_STATE_TOO_WET  # TooHumid

    @property
    def is_light_on(self) -> bool:
        """Return True if detected light."""
        return self.light > 0

    @property
    def is_leaking(self) -> bool:
        """Return True if detected water leak - applicable for water sensor only."""
        return self.tag_type == CONST.WIRELESSTAG_TYPE_WATER and self.moisture > 0

    @property
    def is_battery_low(self) -> bool:
        """Return True if detected low battery level."""
        return self.battery_volts <= self.low_battery_threshold

    @property
    def ambient_temperature(self):
        """Return ambient temperature value. Outdoor Probe only."""
        return self.humidity

    @property
    def revision(self) -> int:
        """Return revision of sensortag hardware."""
        return self._info['rev']

    @property
    def has_sen0227(self) -> bool:
        """Return if SEN0227 is connected."""
        return self._info['shorted']

    @property
    def has_ds18(self) -> bool:
        """Return if ds18 is connected."""
        return self._info['ds18']

    @property
    def product_version(self) -> int:
        """Return product variation variation."""
        return self.extract_last_bits(self.revision, 4)

    @property
    def human_readable_name(self):
        """Human readable tag name."""
        names_map = {
            13: "Tag w/13b Temperature",
            26: "ALS Pro Tag",
            32: "Water/Moisture Sensor",
            42: "Outdoor Probe",
            72: "PIR Sensor",
        }

        hw_revision = hex(self.hw_revision)[2:].upper()
        if self.tag_type in names_map:
            return '{} rev.{}'.format(names_map[self.tag_type], hw_revision)

        return 'Tag type {} rev.{}'.format(self.tag_type, hw_revision)

    @property
    def outdoor_probe_has_ambient_temperature(self) -> bool:
        """Return if outdoor probe tag has ambient temperature."""
        # .rev & 0xF:    shows which product it is
        # 0xD:  Outdoor Probe Basic.
        #  Accepts DS18B20 (read tip temperature in .temperature only)
        # or SEN0227  (read tip temperature in .temperature and tip humidity in .cap)
        # 0xF:   Outdoor Probe Thermocouple.
        #   Accepts DS18B20 (read tip temperature in .temperature and ambient temperature in .cap)
        #   or Thermocouple (read tip temperature in .temperature and ambient temperature in .cap)
        #   or SEN0227  (read tip temperature in .temperature and tip humidity in .cap)
        # .shorted:  1 if SEN0227 is connected
        # .ds18:  1 if DS18B20 is connected
        probe_ambient_map = {
            0xD: False,  # 0xD:  Outdoor Probe Basic.
            0xF: not self.has_sen0227  # 0xF:  Outdoor Probe Thermocouple.
        }
        probe_type = self.product_version
        return probe_ambient_map[probe_type] if probe_type in probe_ambient_map else False

    @property
    def outdoor_probe_has_humidity(self) -> bool:
        """Return if outdoor probe tag tip humidity."""
        probe_humidity_map = {
            0xD: not self.has_ds18,  # 0xD:  Outdoor Probe Basic.
            0xF: self.has_sen0227  # 0xF:  Outdoor Probe Thermocouple.
        }
        probe_type = self.product_version
        return probe_humidity_map[probe_type] if probe_type in probe_humidity_map else True

    @staticmethod
    def extract_last_bits(integer, amount_of_bits) -> int:
        """Return last bits from integer."""
        binary = bin(integer)
        binary = binary[2:]

        end = len(binary)
        start = end - amount_of_bits

        sub_str = binary[start: end]
        return int(sub_str, 2)

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

    def event_for_type(self, event_type) -> BinaryEvent:
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
                CONST.SENSOR_HUMIDITY],
            CONST.WIRELESSTAG_TYPE_OUTDOOR_PROBE: [
                CONST.SENSOR_TEMPERATURE,
                CONST.SENSOR_HUMIDITY],
            CONST.WIRELESSTAG_TYPE_WEMO_DEVICE: []
        }

        tag_type = self.tag_type
        allowed_types = (
            sensors_per_tag_type[tag_type] if tag_type in sensors_per_tag_type
            else all_sensors)

        if self.tag_type == CONST.WIRELESSTAG_TYPE_OUTDOOR_PROBE:
            if self.outdoor_probe_has_ambient_temperature:
                allowed_types.append(CONST.SENSOR_AMBIENT_TEMPERATURE)
            if not self.outdoor_probe_has_humidity:
                allowed_types.remove(CONST.SENSOR_HUMIDITY)

        return allowed_types

    def sensor_for_type(self, sensor_type) -> Sensor:
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

    def detected_events(self, old_tag):
        """Identify if current tag has triggered binary event."""
        if old_tag is None:
            return None

        events = []
        if self.motion_state != old_tag.motion_state:
            event = BinaryEvent.make_state_event(self)
            if event is not None:
                events.append(event)

        if self.is_leaking != old_tag.is_leaking:
            event = BinaryEvent.make_event(CONST.EVENT_MOISTURE, self)
            events.append(event)

        if self.moisture_sensor_state != old_tag.moisture_sensor_state:
            event = self._make_humidity_event(old_tag)
            if event is not None:
                events.append(event)

        if self.temperature_sensor_state != old_tag.temperature_sensor_state:
            event = self._make_temperature_event(old_tag)
            if event is not None:
                events.append(event)

        if self.light_sensor_state != old_tag.light_sensor_state:
            event = BinaryEvent.make_event(CONST.EVENT_LIGHT, self)
            events.append(event)

        if self.is_battery_low != old_tag.is_battery_low:
            event = BinaryEvent.make_event(CONST.EVENT_BATTERY, self)
            events.append(event)

        if self.is_in_range != old_tag.is_in_range:
            event = BinaryEvent.make_event(CONST.EVENT_PRESENCE, self)
            events.append(event)

        return events

    @property
    def humidity_event_type(self):
        """Return current humidity event type."""
        spec = {CONST.HUMIDITY_STATE_TOO_DRY: CONST.EVENT_DRY,
                CONST.HUMIDITY_STATE_TOO_WET: CONST.EVENT_WET}
        event_type = None
        if self.humidity_sensor_state in spec:
            event_type = spec[self.humidity_sensor_state]
        return event_type

    def _make_humidity_event(self, old_tag) -> BinaryEvent:
        """Make humidity binary event."""
        # NA(0) or Disarmed (1) or Normal(2) or TooDry(3) or TooHumid(4) or ThresholdPending
        event_type = self.humidity_event_type
        if self.humidity_sensor_state == CONST.HUMIDITY_STATE_NORMAL:  # Normal(2) then check previous state
            event_type = old_tag.humidity_event_type

        return BinaryEvent.make_event(event_type, self)

    @property
    def temperature_event_type(self):
        """Return current temperature event type."""
        spec = {CONST.TEMP_STATE_TOO_HIGH: CONST.EVENT_HEAT,
                CONST.TEMP_STATE_TOO_LOW: CONST.EVENT_COLD}
        event_type = None
        if self.temperature_sensor_state in spec:
            event_type = spec[self.temperature_sensor_state]
        return event_type

    def _make_temperature_event(self, old_tag) -> BinaryEvent:
        """Make temperature binary event."""
        # Disarmed(0) or Normal(1) or TooHigh(2) or TooLow(3) or ThresholdPending(4)
        event_type = self.temperature_event_type
        if self.temperature_sensor_state == CONST.TEMP_STATE_NORMAL:  # Normal(1)
            event_type = old_tag.temperature_event_type

        return BinaryEvent.make_event(event_type, self)

    def __getattr__(self, key):
        """Return proxy models for subscripting support."""
        if key == 'sensor':
            return SensorProxy(self)
        elif key == 'event':
            return BinaryEventProxy(self)
        else:
            raise AttributeError

    def __repr__(self):
        """Return string representation of tag."""
        # Water/Moisture Sensor supports water and temperature
        if self.tag_type == CONST.WIRELESSTAG_TYPE_WATER:
            return '{} temp: {} leak: {}'.format(self.name, self.temperature, self.is_leaking)
        # ALS Pro (8bit)
        elif self.tag_type == CONST.WIRELESSTAG_TYPE_ALSPRO:
            return '{} temp: {} humidity: {} lux: {}'.format(self.name, self.temperature, self.humidity, self.light)
        elif self.tag_type == CONST.WIRELESSTAG_TYPE_OUTDOOR_PROBE and self.outdoor_probe_has_ambient_temperature:
            return '{} temp: {} ambient temp: {}'.format(self.name, self.temperature, self.ambient_temperature)

        # use 13-bit tag supports temp/motion/humidity as fallback for everything else
        return '{} temp: {} humidity: {}'.format(self.name, self.temperature, self.humidity)
