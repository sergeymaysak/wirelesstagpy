# Wireless Sensor Tags python

A simple python wrapper library for Wireless Sensor Tag platform (http://wirelesstag.net).

Supports getting data for registered by end user sensor tags.
mytaglist.com account credentials are needed to use this lib.
Enabling tags sharing is not required.

Verified with 13-bit motion/temperature/humidity tags.

# Installation

# Development notes
See http://wirelesstag.net/apidoc.html for API details.

# Usage

```python

import wirelesstagpy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
sensors = api.load_tags()
for (uuid, sensor) in sensors.items():
    print('Loaded sensor: {}, temp: {}, humidity: {} probe taken: {}'.format(sensor.name, sensor.temperature, sensor.humidity, sensor.time_since_last_update))

```

# Disclaimer
"Wireless Sensor Tags", "KumoSensor" and "Kumostat" are trademarks of Cao Gadgets LLC,
see www.wirelesstag.net for more information.

I am in no way affiliated with Cao Gadgets LLC.

# Copyright
See [LICENSE](.LICENSE)

