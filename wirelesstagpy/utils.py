#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Utilities functions for wirelesstagpy module.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/8/2018.
"""

from datetime import timedelta, datetime

EPOCH_AS_FILETIME = 116444736000000000


def convert_filetime_to_dt(file_time):
    """Convert filetime to datetime."""
    u_microseconds = (file_time - EPOCH_AS_FILETIME) // 10
    return datetime(1970, 1, 1) + timedelta(microseconds=u_microseconds)
