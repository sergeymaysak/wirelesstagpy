#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module with tests for cloud push API in wirelesstags platform."""

import json
from xml.etree import ElementTree

import test.mock as MOCK
import requests_mock
import tl.testing.thread

import wirelesstagpy
import wirelesstagpy.constants as CONST

USERNAME = 'foobar'
PASSWORD = 'deadbeef'


class TestCloudPush(tl.testing.thread.ThreadAwareTestCase):
    """Tests for Cloud Push logic."""

    def setUp(self):
        """Set up wirelesstags platform module."""
        self.platform = wirelesstagpy.WirelessTags(username=USERNAME, password=PASSWORD)

    def tearDown(self):
        """Clean up after each test."""
        self.platform = None

    @requests_mock.mock()
    def test_cloud_push(self, m):
        """Test cloud push logic."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.REQUEST_CLOUD_PUSH_UPDATE_URL, text=MOCK.CLOUD_PUSH_UPDATE_RESPONSE)

        local_platform = self.platform

        def push_callback(tags):
            """Local push callback."""
            self.assertTrue(local_platform.is_monitoring)
            self.assertTrue(len(tags) == 1)
            local_platform.stop_monitoring()
            self.assertFalse(local_platform.is_monitoring)

        with tl.testing.thread.ThreadJoiner(1):
            self.platform.start_monitoring(push_callback)
            # try to run it again
            if self.platform.is_monitoring is True:
                self.platform.start_monitoring(push_callback)
        self.assertFalse(self.platform.is_monitoring)
        self.platform.stop_monitoring()
        self.assertFalse(self.platform.is_monitoring)

    @requests_mock.mock()
    def test_cloud_push_failed(self, m):
        """Test cloud push logic."""
        m.post(CONST.SIGN_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.IS_SIGNED_IN_URL, text=MOCK.LOGIN_RESPONSE)
        m.post(CONST.REQUEST_CLOUD_PUSH_UPDATE_URL, status_code=500)

        local_platform = self.platform

        def push_callback(tags):
            pass

        with tl.testing.thread.ThreadJoiner(1):
            self.platform.start_monitoring(push_callback)
            local_platform.stop_monitoring()
        self.assertFalse(self.platform.is_monitoring)

    def test_soup_parsing(self):
        """Test for parsing arrived soap payload on cloud push."""
        root = ElementTree.fromstring(MOCK.CLOUD_PUSH_UPDATE_RESPONSE)
        raw_tags = root.find(".//{http://mytaglist.com/ethComet}GetNextUpdate2Result")
        tags = json.loads(raw_tags.text)
        self.assertTrue(len(tags) == 1)
