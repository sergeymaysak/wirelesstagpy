#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module with tests for outdoor probe sensor in wirelesstags platform."""

import test.mock as MOCK
import unittest

import wirelesstagpy
import wirelesstagpy.constants as CONST

USERNAME = 'foobar'
PASSWORD = 'deadbeef'


def extract_last_bits(integer, amount_of_bits) -> int:
    """Return last bits from integer."""
    binary = bin(integer)
    binary = binary[2:]

    end = len(binary)
    start = end - amount_of_bits

    sub_str = binary[start: end]
    return int(sub_str, 2)


class TestOutdoorProbe(unittest.TestCase):
    """Tests for Cloud Push logic."""

    def setUp(self):
        """Set up wirelesstags platform module."""
        self.platform = wirelesstagpy.WirelessTags(username=USERNAME, password=PASSWORD)
        self.tag_outdoor = wirelesstagpy.SensorTag(MOCK.OUTDOOR_PROBE, self.platform)
        self.platform._tags["fake-1"] = self.tag_outdoor  # pylint: disable=protected-access

    def tearDown(self):
        """Clean up after each test."""
        self.platform = None
        self.tag_outdoor = None

    def test_probe_type(self):
        """Test probe type."""
        rev = 159
        last_bits = extract_last_bits(rev, 4)
        print("last bits {}".format(last_bits))
        self.assertEqual(last_bits, 0xF)

        rev = 158
        last_bits = extract_last_bits(rev, 4)
        self.assertEqual(last_bits, 0xE)

        rev = 157
        last_bits = extract_last_bits(rev, 4)
        self.assertEqual(last_bits, 0xD)

    def test_ambient_tmeperature_sensor(self):
        """Test outdoor probe ambient sensor."""
        self.assertEqual(self.tag_outdoor.has_ambient_temperature, True)

        sensor = self.tag_outdoor.sensor[CONST.SENSOR_AMBIENT_TEMPERATURE]
        self.assertIsNotNone(sensor)
        self.assertEqual(sensor.value, 23.43)

        self.assertIn('ambient temp:', str(self.tag_outdoor))

    def test_supported_sensor_types(self):
        """Test allowed outdoor probe sensor types generation."""
        allowed = self.tag_outdoor.allowed_sensor_types
        self.assertIn(CONST.SENSOR_AMBIENT_TEMPERATURE, allowed)
        self.assertIn(CONST.SENSOR_TEMPERATURE, allowed)
        self.assertNotIn(CONST.SENSOR_HUMIDITY, allowed)
        self.assertNotIn(CONST.SENSOR_LIGHT, allowed)
