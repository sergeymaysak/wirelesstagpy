# WirelessSensorTags  [![Build Status](https://travis-ci.org/sergeymaysak/wirelesstagpy.svg?branch=master)](https://travis-ci.org/sergeymaysak/wirelesstagpy) [![Coverage Status](https://coveralls.io/repos/github/sergeymaysak/wirelesstagpy/badge.svg?branch=master)](https://coveralls.io/github/sergeymaysak/wirelesstagpy?branch=master) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wirelesstagpy.svg)

A simple python wrapper library for Wireless Sensor Tag platform (http://wirelesstag.net).

Supports getting data for registered by end user sensor tags.
mytaglist.com account credentials are needed to use this lib.
Enabling tags sharing is not required.

Verified with 13-bit motion/temperature/humidity tags.

# Installation

```shell
pip3 install wirelesstagpy
```

# Development notes
See http://wirelesstag.net/apidoc.html for API details.

# Usage

```python

import wirelesstagpy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
sensors = api.load_tags()
for (uuid, tag) in sensors.items():
    print('Loaded sensor: {}, temp: {}, humidity: {} probe taken: {}'.format(
                tag.name, tag.temperature, 
                tag.humidity, tag.time_since_last_update))

```

# Disclaimer
"Wireless Sensor Tags", "KumoSensor" and "Kumostat" are trademarks of Cao Gadgets LLC,
see www.wirelesstag.net for more information.

I am in no way affiliated with Cao Gadgets LLC.

# Copyright
See [LICENSE](LICENSE)

