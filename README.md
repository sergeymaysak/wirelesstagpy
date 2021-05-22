# WirelessSensorTags  [![Build Status](https://travis-ci.org/sergeymaysak/wirelesstagpy.svg?branch=master)](https://travis-ci.org/sergeymaysak/wirelesstagpy) [![Coverage Status](https://coveralls.io/repos/github/sergeymaysak/wirelesstagpy/badge.svg?branch=master)](https://coveralls.io/github/sergeymaysak/wirelesstagpy?branch=master) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wirelesstagpy.svg) ![PyPi - Version](https://img.shields.io/pypi/v/wirelesstagpy.svg)

A simple python wrapper library for Wireless Sensor Tag platform (`http://wirelesstag.net`).

Supports getting data for registered by end user sensor tags.
wirelesstag.net account credentials are needed to use this lib.
Enabling tags sharing is not required.

Verified with:

- 13-bit motion/temperature/humidity tags (type 13)
- Water/Moisture tags (type 32)
- ALS Pro tag (type 26)
- PIR Kumo sensor (type 72)

## Installation

```shell
pip3 install wirelesstagpy
```

## Development notes

See [apidoc.html](http://wirelesstag.net/apidoc.html) for API details.

## Usage

### Fetch all tags

```python

import wirelesstagpy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
tags = api.load_tags()
for (uuid, tag) in tags.items():
    print('Loaded tag: {}, temp: {}, humidity: {} probe taken: {}'.format(
                tag.name, tag.temperature,
                tag.humidity, tag.time_since_last_update))

```

## Install custom push notifications

Wireless Sensor Tags platforms allows to setup custom url calls for set of specific events.

```python


import wirelesstagpy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
notifications = [
    NotificationConfig('update', {
        'url': 'http://some_local_ip/update_tags',
        'verb': 'POST'
        'disabled': False,
        'nat': True
    })
]

# install notification for tag with id=1 only
# use it you have only one tag manager
succeed = api.install_push_notification(1, notifications, False)

# if you have multiple tag managers you need specify its 'mac' stored in each tag as following
succeed = api.install_push_notification(sensor.tag_id, notifications, False,
                                        sensor.tag_manager_mac)

```

## Monitor push events from cloud

Wireless Sensor Tags platform allows to monitor state of sensors with push notification on change right from cloud.

```python

import wirelesstagspy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
def callback(tags_spec, events_spec):
    for (uuid, tag) in tags_spec.items():
        if uuid in events_spec:
            events = events_spec[uuid]
            print("triggered events: {}".format(events))
        print("updated tag: {}".format(tag))

# starts long running thread with getting updates from cloud immidiately when change happens.
# it is not a polling, but rather a similar to WebSockets get update logic
api.start_monitoring(callback)

```

## Arm/Disarm sensor monitoring for specific event

Supported events include: motion, temperature, humidity, light

```python

import wirelesstagpy

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')

# arm humidity monitoring for tag with id 1,
# returned instance is updated SensorTag
sensor = api.arm_humidity(1)

# Disarm it
sensor = api.disarm_humidity(1)

# Specify tag manager if you have multiple tag managers
sensor = api.arm_humidity(sensor.tag_id, sensor.tag_manager_mac)

```

## Working with sensors and binary events

Single tag holds notion of multiple sensors and binary events.
Each sensor is entity representing single sensing metric such as temperature, humidity, moisture, light or motion.
You can get list of supported sensors and binary events by calling `tag.allowed_sensor_types` for sensors,
`tag.supported_binary_events_types` for binary events.
Also you can query tag on list of supported monitoring conditions that can be represented as switches to be armed/disarmed by calling `tag.allowed_monitoring_types`.

Handling sensors:

```python

import wirelesstagpy
import wirelesstagpy.constants as CONST

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
tags = api.load_tags()

# get temperature sensor value for tag
for (uuid, tag) in tags.items():
    sensor = tag.sensor[CONST.SENSOR_TEMPERATURE]
    if sensor is not None:
        print('{} temperature: {}'.format(tag.name, sensor.value))

```

Handling binary events:

```python

import wirelesstagpy
import wirelesstagpy.constants as CONST

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
tags = api.load_tags()

# get motion binary event state for each tag
for (uuid, tag) in tags.items():
    if CONST.EVENT_MOTION in tag.supported_binary_events_types:
        event = tag.event[CONST.EVENT_MOTION]
        print('tag {} event state: {}'.format(tag.name, event.is_state_on))

```

Use binary events to build custom push notifications configurations

```python

import wirelesstagpy
import wirelesstagpy.constants as CONST

api = wirelesstagpy.WirelessTags(username='login_email', password='your_password')
tags = api.load_tags()
tag = tags['uuid-of-tag-in-question']
event = tag.event[CONST.EVENT_MOISTURE]
if event is not None:
    configs = event.build_notifications('http://path_to_post', tag.tag_manager_mac)
    # install it for any tags of tag manager
    succeed = api.install_push_notification(0, configs, True,
                                            tag.tag_manager_mac)
```

## Disclaimer

"Wireless Sensor Tags", "KumoSensor" and "Kumostat" are trademarks of Cao Gadgets LLC,
see www.wirelesstag.net for more information.

I am in no way affiliated with Cao Gadgets LLC.

## Copyright

See [LICENSE](LICENSE)
