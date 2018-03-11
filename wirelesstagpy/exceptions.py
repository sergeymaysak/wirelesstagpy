#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags exceptions."""


class WirelessTagsException(Exception):
    """WirelessTags exception."""

    def __init__(self, message):
        """Initialize WirelessTagsException."""
        super(WirelessTagsException, self).__init__(message)
        self.message = message
