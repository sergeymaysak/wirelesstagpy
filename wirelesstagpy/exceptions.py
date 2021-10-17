#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags exceptions."""


class WirelessTagsException(Exception):
    """WirelessTags exception."""

    def __init__(self, message):
        """Initialize WirelessTagsException."""
        super().__init__(message)
        self.message = message


class WirelessTagsWrongCredentials(WirelessTagsException):
    """WirelessTags email or password wrong exception."""

    def __init__(self):
        """Initialize WirelessTagsWrongCredentials."""
        super().__init__("Unable to login to wirelesstags.net - check your credentials")


class WirelessTagsConnectionError(WirelessTagsException):
    """WirelessTags generic connection error."""

    def __init__(self):
        """Initialize WirelessTagsConnectionError."""
        super().__init__("Connection error.")
