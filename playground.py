#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WirelessTags examples runner."""
import asyncio
import wirelesstagpy

loop = asyncio.get_event_loop()
platform = wirelesstagpy.WirelessTags(username='email', password='passwd')

def callback(sensors):
    """Callback on cloud push update."""
    print("updated sensors: {}".format(sensors))

platform.start_monitoring(callback)
print("started push updates")

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    platform.stop_monitoring()
    print('stopped monitoring')
loop.close()
