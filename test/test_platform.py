#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module with tests for wirelesstag platform."""

import unittest

import test.mock as MOCK
import requests_mock

import wirelesstagpy
import wirelesstagpy.constants as CONST

USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestWirelessTags(unittest.TestCase):
    """Tests for WirelessTags."""

    def setUp(self):
        """Set up wirelesstags platform module."""
        self.platform_no_cred = wirelesstagpy.WirelessTags(username='', password='')
        self.platform = wirelesstagpy.WirelessTags(username=USERNAME, password=PASSWORD)

    def tearDown(self):
        """Clean up after each test."""
        self.platform = None
        self.platform_no_cred = None

    @requests_mock.mock()
    def tests_full_data_load(self, m):
        """Test full data logic."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.GET_TAGS_URL, text=MOCK.TAGS_LIST_RESPONSE)

        tags = self.platform.load_tags()
        self.assertTrue(list(tags.keys()))
        self.assertTrue(self.platform.use_celsius)

        for uuid, sensor in tags.items():
            self.assertEqual(uuid, sensor.uuid)

            self.assertIsNotNone(sensor.name)
            self.assertIsNotNone(sensor.uuid)
            self.assertTrue(sensor.in_celcius)

            self.assertIsNotNone(sensor.temperature)
            self.assertTrue(isinstance(sensor.temperature, float))

            self.assertIsNotNone(sensor.humidity)
            self.assertTrue(isinstance(sensor.humidity, float))

            self.assertIsNotNone(sensor.battery_remaining)

            self.assertIsNotNone(sensor.battery_volts)
            self.assertIsNotNone(sensor.tag_type)
            self.assertIsNotNone(sensor.comment)
            self.assertIsNotNone(sensor.is_alive)
            self.assertIsNotNone(sensor.signal_straight)
            self.assertIsNotNone(sensor.beep_option)
            self.assertIsNotNone(sensor.is_in_range)
            self.assertIsNotNone(sensor.hw_revision)
            self.assertIsNotNone(sensor.sw_version)
            self.assertIsNotNone(sensor.power_consumption)
            print("tag: {} last updated: {}".format(sensor, sensor.time_since_last_update))

    @requests_mock.mock()
    def test_failed_login(self, m):
        """Verify handling of incorrect credentials."""
        m.post(CONST.SIGN_IN_URL, status_code=500)
        with self.assertRaises(wirelesstagpy.WirelessTagsException):
            tags = self.platform_no_cred.load_tags()
            print('tags: {}'.format(tags))

    @requests_mock.mock()
    def test_failed_load_tags(self, m):
        """Verify exception handling while server is not responding."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.GET_TAGS_URL, text='{no really valid payload}', status_code=500)

        tags = self.platform.load_tags()
        self.assertFalse(tags.keys())

    @requests_mock.mock()
    def test_check_of_sign_in_status(self, m):
        """Verify exception handling while unable to get respnse on signin status."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text='{no really valid payload}', status_code=500)
        m.post(CONST.GET_TAGS_URL, text=MOCK.TAGS_LIST_RESPONSE)

        tags = self.platform.load_tags()
        description = str(self.platform)
        self.assertTrue(description.startswith('WirelessTagsPlatform: using celsius'))
        print('platform: {}'.format(description))
        self.assertTrue(tags.keys())
