#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module with tests for wirelesstag platform."""

import unittest

import test.mock as MOCK
import requests_mock


import wirelesstagpy
import wirelesstagpy.constants as CONST
from wirelesstagpy.sensortag import SensorTag
from wirelesstagpy.notificationconfig import NotificationConfig

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
            self.assertIsNotNone(sensor.tag_manager_mac)

            self.assertIsNotNone(sensor.temperature)
            self.assertTrue(isinstance(sensor.temperature, float))

            self.assertIsNotNone(sensor.humidity)
            self.assertTrue(isinstance(sensor.humidity, float))

            self.assertIsNotNone(sensor.battery_remaining)

            self.assertIsNotNone(sensor.battery_volts)
            self.assertIsNotNone(sensor.tag_type)
            self.assertIsNotNone(sensor.comment)
            self.assertIsNotNone(sensor.is_alive)
            self.assertIsNotNone(sensor.signal_strength)
            self.assertIsNotNone(sensor.beep_option)
            self.assertIsNotNone(sensor.is_in_range)
            self.assertIsNotNone(sensor.hw_revision)
            self.assertIsNotNone(sensor.sw_version)
            self.assertIsNotNone(sensor.power_consumption)

            self.assertFalse(sensor.is_motion_sensor_armed)
            self.assertFalse(sensor.is_humidity_sensor_armed)
            self.assertFalse(sensor.is_temperature_sensor_armed)
            self.assertFalse(sensor.is_moisture_sensor_armed)
            self.assertTrue(sensor.moisture_sensor_state == 0)
            self.assertFalse(sensor.is_light_sensor_armed)
            print("tag: {} last updated: {}".format(sensor, sensor.time_since_last_update))

    def test_alspro_tag_binary_states(self):
        """Test avaiable binary states for als pro tag."""
        tag = SensorTag(MOCK.ALS_PRO, self.platform, '0d0d0d0d0d0d')
        self.assertTrue(tag.is_moved)
        self.assertFalse(tag.is_door_open)
        self.assertTrue(tag.is_cold)
        self.assertFalse(tag.is_heat)
        self.assertFalse(tag.is_too_dry)
        self.assertFalse(tag.is_too_humid)
        self.assertFalse(tag.is_leaking)
        self.assertTrue(tag.is_light_on)
        self.assertFalse(tag.is_battery_low)
        self.assertIsNotNone(str(tag))
        self.assertIsNotNone(tag.tag_manager_mac)
        self.assertIsNotNone(tag.human_readable_name)

    def test_water_tag_binary_states(self):
        """Test avaiable binary states for als pro tag."""
        tag = SensorTag(MOCK.WATERSENSOR, self.platform, '0d0d0d0d0d0d')
        self.assertFalse(tag.is_moved)
        self.assertFalse(tag.is_door_open)
        self.assertFalse(tag.is_cold)
        self.assertFalse(tag.is_heat)
        self.assertFalse(tag.is_too_dry)
        self.assertFalse(tag.is_too_humid)
        self.assertTrue(tag.is_leaking)
        self.assertFalse(tag.is_light_on)
        self.assertFalse(tag.is_battery_low)
        self.assertIsNotNone(str(tag))
        self.assertIsNotNone(tag.tag_manager_mac)
        self.assertIsNotNone(tag.human_readable_name)

    def test_13bit_tag_binary_states(self):
        """Test avaiable binary states for als pro tag."""
        tag = SensorTag(MOCK.BITS13, self.platform, '0d0d0d0d0d0d')
        self.assertFalse(tag.is_moved)
        self.assertTrue(tag.is_door_open)
        self.assertFalse(tag.is_cold)
        self.assertTrue(tag.is_heat)
        self.assertFalse(tag.is_too_dry)
        self.assertTrue(tag.is_too_humid)
        self.assertFalse(tag.is_leaking)
        self.assertFalse(tag.is_light_on)
        self.assertTrue(tag.is_battery_low)
        self.assertIsNotNone(str(tag))
        self.assertIsNotNone(tag.tag_manager_mac)
        self.assertIsNotNone(tag.human_readable_name)

    def test_unknown_sensor_name(self):
        """Test avaiable binary states for als pro tag."""
        tag = SensorTag(MOCK.TAG_UNKNOWN, self.platform, '0d0d0d0d0d0d')
        self.assertEquals(tag.human_readable_name, "Tag type 15 rev.AF")


    @requests_mock.mock()
    def test_failed_login(self, m):
        """Verify handling of incorrect credentials."""
        m.post(CONST.SIGN_IN_URL, text='unauthorized', status_code=500)
        with self.assertRaises(wirelesstagpy.WirelessTagsWrongCredentials):
            tags = self.platform_no_cred.load_tags()
            print('tags: {}'.format(tags))

    @requests_mock.mock()
    def test_failed_login_connection_failed(self, m):
        """Verify handling of incorrect credentials."""
        m.post(CONST.SIGN_IN_URL, status_code=503)
        with self.assertRaises(wirelesstagpy.WirelessTagsConnectionError):
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

    @requests_mock.mock()
    def test_arm_disarm_motion(self, m):
        """Verify arm/disarm basic behaviour."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_MOTION_URL, text=MOCK.ARM_MOTION_RESPONSE)
        m.post(CONST.DISARM_MOTION_URL, text=MOCK.DISARM_MOTION_RESPONSE)

        sensor = self.platform.arm_motion(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertTrue(sensor.is_motion_sensor_armed)

        sensor = self.platform.disarm_motion(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertFalse(sensor.is_motion_sensor_armed)

    @requests_mock.mock()
    def test_arm_disarm_motion_with_mac(self, m):
        """Verify arm/disarm basic behaviour."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_MOTION_URL, text=MOCK.ARM_MOTION_RESPONSE)
        m.post(CONST.DISARM_MOTION_URL, text=MOCK.DISARM_MOTION_RESPONSE)

        sensor = self.platform.arm_motion(1, '0d0d0d0d0d0d')
        self.assertEqual(sensor.tag_id, 1)
        self.assertEqual(sensor.tag_manager_mac, '0d0d0d0d0d0d')
        self.assertTrue(sensor.is_motion_sensor_armed)

        sensor = self.platform.disarm_motion(1, '0d0d0d0d0d0d')
        self.assertEqual(sensor.tag_id, 1)
        self.assertEqual(sensor.tag_manager_mac, '0d0d0d0d0d0d')
        self.assertFalse(sensor.is_motion_sensor_armed)

    @requests_mock.mock()
    def test_arm_disarm_temperature(self, m):
        """Verify arm/disarm temperature monitoring."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_TEMPERATURE_URL, text=MOCK.ARM_TEMP_RESPONSE)
        m.post(CONST.DISARM_TEMPERATURE_URL, text=MOCK.DISARM_TEMP_RESPONSE)

        sensor = self.platform.arm_temperature(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertTrue(sensor.is_temperature_sensor_armed)

        sensor = self.platform.disarm_temperature(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertFalse(sensor.is_temperature_sensor_armed)

    @requests_mock.mock()
    def test_arm_disarm_humidity(self, m):
        """Verify arm/disarm temperature monitoring."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_HUMIDITY_URL, text=MOCK.ARM_HUMIDITY_RESPONSE)
        m.post(CONST.DISARM_HUMIDITY_URL, text=MOCK.DISARM_HUMIDITY_RESPONSE)

        sensor = self.platform.arm_humidity(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertTrue(sensor.is_humidity_sensor_armed)

        sensor = self.platform.disarm_humidity(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertFalse(sensor.is_humidity_sensor_armed)

    @requests_mock.mock()
    def test_arm_disarm_light(self, m):
        """Verify arm/disarm temperature monitoring."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_LIGHT_URL, text=MOCK.ARM_LIGHT_RESPONSE)
        m.post(CONST.DISARM_LIGHT_URL, text=MOCK.DISARM_LIGHT_RESPONSE)

        sensor = self.platform.arm_light(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertTrue(sensor.is_light_sensor_armed)

        sensor = self.platform.disarm_light(1)
        self.assertEqual(sensor.tag_id, 1)
        self.assertFalse(sensor.is_light_sensor_armed)

    @requests_mock.mock()
    def test_arm_disarm_failed(self, m):
        """Verify arm/disarm temperature monitoring."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.ARM_LIGHT_URL, text='{no really valid payload}')

        sensor = self.platform.arm_light(1)
        self.assertIsNone(sensor)

    @requests_mock.mock()
    def test_fetch_push_notifications(self, m):
        """Test fetch installed push notifications."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.LOAD_EVENT_URL_CONFIG_URL, text=MOCK.LOAD_EVENT_URL_CONFIG_RESPONSE)

        notifications = self.platform.fetch_push_notifications(1)
        self.assertEqual(len(notifications), 22)

        enabled_notification = list(filter(lambda x: x.is_enabled, notifications))
        self.assertEqual(len(enabled_notification), 1)

        config = enabled_notification[0]
        self.assertEqual(config.name, 'update')
        self.assertEqual(config.is_local, True)
        self.assertEqual(config.verb, 'POST')
        self.assertEqual(config.content, 'message')
        self.assertEqual(config.url, 'http://host_name/update')

    @requests_mock.mock()
    def test_fail_fetch_notifications(self, m):
        """Test for catching errors logic inside fetch method."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.LOAD_EVENT_URL_CONFIG_URL, text='kinda failed', status_code=500)

        notifications = self.platform.fetch_push_notifications(1)
        self.assertEqual(len(notifications), 0)

    def test_notification(self):
        """Test NotificationConfig properties."""
        config = NotificationConfig('update', MOCK.UPDATE_NOTIFICATION_CONFIG)

        self.assertEqual(config.name, 'update')
        self.assertEqual(config.is_local, True)
        self.assertEqual(config.verb, 'POST')
        self.assertEqual(config.content, "{\"name\":\"{0}\",\"id\":{1},\"temp\": {2}, \"cap\":{3},\"lux\":{4}}")
        self.assertEqual(config.url, 'http://10.10.0.2/api/events/update_tags')
        self.assertIsNotNone(str(config))

    @requests_mock.mock()
    def test_install_notifications(self, m):
        """Test install push notifications."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.LOAD_EVENT_URL_CONFIG_URL, text=MOCK.LOAD_EVENT_URL_CONFIG_RESPONSE)
        m.post(CONST.SAVE_EVENT_URL_CONFIG_URL, text=MOCK.LOAD_EVENT_URL_CONFIG_RESPONSE)

        notifications = [
            NotificationConfig("update", MOCK.UPDATE_NOTIFICATION_CONFIG)
        ]

        result = self.platform.install_push_notification(1, notifications, False)
        self.assertTrue(result)
        print('succeed: ', result)

    @requests_mock.mock()
    def test_fail_setup_notifications(self, m):
        """Test for catching errors logic inside install notifications method."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.LOAD_EVENT_URL_CONFIG_URL, text='kinda failed', status_code=500)

        notifications = [
            NotificationConfig("update", MOCK.UPDATE_NOTIFICATION_CONFIG)
        ]
        result = self.platform.install_push_notification(1, notifications, False)
        self.assertFalse(result)

    def test_leak_binary_event(self):
        """Test water leak binary events logic."""
        mac = '0d0d0d0d0d0d'
        tag = SensorTag(MOCK.WATERSENSOR, self.platform, mac)

        event = tag.event[CONST.EVENT_WET]
        self.assertIsNone(event)

        event = tag.event[CONST.EVENT_MOISTURE]
        self.assertIsNotNone(event)
        self.assertTrue(event.is_state_on)

        url = 'http://10.10.0.2/api/events/update_tags'
        notifications = event.build_notifications(url, mac)
        self.assertTrue(len(notifications) == 2)

        config = notifications[0]
        self.assertTrue(config.name in ['water_detected', 'water_dried'])
        self.assertTrue(config.is_enabled)
        self.assertTrue(config.is_local)
        self.assertEqual(config.url, url)
        self.assertEqual(config.verb, 'POST')

    def test_motion_binary_event(self):
        """Test motion binary event for PIR sensor."""
        mac = '12'
        tag = SensorTag(MOCK.PIRSENSOR, self.platform, mac)
        event = tag.event[CONST.EVENT_MOTION]
        same_event = tag.event[CONST.EVENT_MOTION]
        self.assertTrue(event == same_event)
        self.assertIsNotNone(event)
        self.assertFalse(event.is_state_on)

        url = 'http://10.10.0.2/api/events/update_tags'
        notifications = event.build_notifications(url, mac)
        self.assertTrue(len(notifications) == 1)

        config = notifications[0]
        self.assertEqual(config.name, 'motion_detected')
        self.assertTrue(config.is_enabled)
        self.assertTrue(config.is_local)
        self.assertEqual(config.url, url)
        self.assertEqual(config.verb, 'POST')

    def test_make_update_event(self):
        """Test logic to create update event push notification."""
        url = 'https://update/tag'
        mac = '12'
        config = NotificationConfig.make_config_for_update_event(url, mac)
        self.assertIsNotNone(config)
        self.assertEqual(config.url, url)
        self.assertEqual(config.verb, 'POST')
        self.assertTrue(config.is_enabled)
        self.assertTrue(config.is_local)

    def test_sensors(self):
        """Test sensors supported by tag."""
        mac = '12'
        tag = SensorTag(MOCK.PIRSENSOR, self.platform, mac)
        sensor = tag.sensor[CONST.SENSOR_TEMPERATURE]
        same_sensor = tag.sensor[CONST.SENSOR_TEMPERATURE]
        self.assertIsNotNone(sensor)
        self.assertTrue(sensor == same_sensor)
        self.assertEqual(sensor.value, 23.924919128417969)
        self.assertIsNotNone(str(sensor))

        event = {'name': 'Kitchen', 'id': 8,
                 'temp': 24.1517391204834, 'cap': 0,
                 'lux': 0, 'mac': '12'}
        value = sensor.value_from_update_event(event)
        self.assertEqual(value, 24.1517391204834)

        value = sensor.value_from_update_event({'name': 'no-exist'})
        self.assertEqual(value, 0)

        no_sensor = tag.sensor[CONST.SENSOR_LIGHT]
        self.assertIsNone(no_sensor)

    def test_switches(self):
        """Test allowed monitoring entities."""
        mac = '12'
        tag = SensorTag(MOCK.PIRSENSOR, self.platform, mac)
        switch_types = tag.allowed_monitoring_types
        self.assertIn(CONST.ARM_TEMPERATURE, switch_types)
        self.assertIn(CONST.ARM_HUMIDITY, switch_types)
        self.assertIn(CONST.ARM_MOTION, switch_types)

    def test_no_sensor_for_subscription(self):
        """Test for non-existing attribute."""
        mac = '12'
        tag = SensorTag(MOCK.PIRSENSOR, self.platform, mac)
        with self.assertRaises(AttributeError):
            no_message = tag.message
            print('message: {}'.format(no_message))
