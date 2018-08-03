"""mocks live here."""

ALS_PRO = {
    "name": "Kitchen",
    "uuid": "fake-1111-2222-4444-111111111111",
    "managerName": "#manager_1",
    "mac": "0D0D0D0D0D0D",
    "slaveId": 1,
    "tagType": 26,
    "eventState": 2,
    "tempEventState": 3,
    "capEventState": 0,
    "lightEventState": 0,
    "temperature": 22.3912296295166,
    "lux": 1000,
    "cap": 36,
    "batteryVolt": 3.05576890659684,
    "LBTh": 2.55
}

BITS13 = {
    "name": "Kitchen",
    "uuid": "fake-1111-2222-4444-111111111111",
    "managerName": "#manager_1",
    "mac": "0D0D0D0D0D0D",
    "slaveId": 1,
    "tagType": 13,
    "eventState": 3,
    "tempEventState": 2,
    "capEventState": 4,
    "lightEventState": 0,
    "temperature": 22.3912296295166,
    "lux": 0,
    "cap": 87,
    "batteryVolt": 2.05576890659684,
    "LBTh": 2.55
}

WATERSENSOR = {
    "name": "Kitchen",
    "uuid": "fake-1111-2222-4444-111111111111",
    "managerName": "#manager_1",
    "mac": "0D0D0D0D0D0D",
    "slaveId": 1,
    "tagType": 32,
    "eventState": 0,
    "tempEventState": 0,
    "capEventState": 0,
    "lightEventState": 0,
    "temperature": 22.3912296295166,
    "lux": 0,
    "cap": 87,
    "batteryVolt": 3.05576890659684,
    "LBTh": 2.55
}

LOGIN_RESPONSE = '''
        {
            "d": {
                "__type": "MyTagList.ethClient+TagManagerSettings",
                "postbackInterval": 600,
                "temp_unit": 0,
                "tzo": -120,
                "serverTime": 131650977888314263,
                "rev": 7,
                "limited": false,
                "rxFilter": 64,
                "optimizeForV2Tag": true,
                "freqTols": [
                    2000,
                    3000,
                    4000,
                    12000,
                    16000
                ],
                "phoneID": "121212121212",
                "loginEmail": null,
                "wsRoot": "https://my.wirelesstag.net/",
                "noWemoSearch": false
            }
        }
        '''


TAGS_LIST_RESPONSE = '''
        {
        "d": [
            {
                "__type": "MyTagList.Tag2",
                "managerName": "#manager_1",
                "mac": "0D0D0D0D0D0D",
                "dbid": 2,
                "mirrors": [],
                "notificationJS": null,
                "name": "Kitchen",
                "uuid": "fake-1111-2222-3333-111111111111",
                "comment": "",
                "slaveId": 4,
                "tagType": 13,
                "lastComm": 131649791032183860,
                "alive": true,
                "signaldBm": -73,
                "batteryVolt": 3.056917542381937,
                "beeping": false,
                "lit": false,
                "migrationPending": false,
                "beepDurationDefault": 5,
                "eventState": 0,
                "tempEventState": 0,
                "OutOfRange": false,
                "lux": 0,
                "temperature": 19.849382400512695,
                "tempCalOffset": 0,
                "capCalOffset": 0,
                "image_md5": null,
                "cap": 45.9866943359375,
                "capRaw": 0,
                "az2": 0,
                "capEventState": 0,
                "lightEventState": 0,
                "shorted": false,
                "thermostat": null,
                "playback": null,
                "postBackInterval": 600,
                "rev": 111,
                "version1": 3,
                "freqOffset": 1,
                "freqCalApplied": 6527,
                "reviveEvery": 4,
                "oorGrace": 2,
                "LBTh": 2.55,
                "enLBN": true,
                "txpwr": 16,
                "rssiMode": false,
                "ds18": false,
                "v2flag": 26,
                "batteryRemaining": 0.97
            },
            {
                "__type": "MyTagList.Tag2",
                "managerName": "#manager_1",
                "mac": "0D0D0D0D0D0D",
                "name": "Hall",
                "uuid": "fake-1111-2222-4444-111111111111",
                "comment": "",
                "slaveId": 0,
                "tagType": 13,
                "lastComm": 131649788589728506,
                "alive": true,
                "signaldBm": -71,
                "batteryVolt": 3.05576890659684,
                "beeping": false,
                "lit": false,
                "migrationPending": false,
                "beepDurationDefault": 1001,
                "eventState": 0,
                "tempEventState": 0,
                "OutOfRange": false,
                "lux": 0,
                "temperature": 22.3912296295166,
                "tempCalOffset": 0,
                "capCalOffset": 0,
                "image_md5": null,
                "cap": 36.27447509765625,
                "capRaw": 0,
                "az2": 0,
                "capEventState": 0,
                "lightEventState": 0,
                "shorted": false,
                "thermostat": null,
                "playback": null,
                "postBackInterval": 600,
                "rev": 111,
                "version1": 3,
                "freqOffset": -357,
                "freqCalApplied": 7541,
                "reviveEvery": 4,
                "oorGrace": 2,
                "LBTh": 2.55,
                "enLBN": true,
                "txpwr": 16,
                "rssiMode": false,
                "ds18": false,
                "v2flag": 26,
                "batteryRemaining": 0.96
            }
        ]
    }
    '''

ARM_MOTION_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 1,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

DISARM_MOTION_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

ARM_TEMP_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 1,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

DISARM_TEMP_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

ARM_HUMIDITY_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 2,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

DISARM_HUMIDITY_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

ARM_LIGHT_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 2,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

DISARM_LIGHT_RESPONSE = '''
    {
        "d": {
            "name": "Living room",
            "uuid": "fake-1111-2222-4444-111111111111",
            "slaveId": 1,
            "tagType": 13,
            "eventState": 0,
            "tempEventState": 0,
            "capEventState": 0,
            "lightEventState": 0,
            "temperature": 22.3912296295166,
            "lux": 0,
            "cap": 36.27447509765625
        }
    }
    '''

LOAD_EVENT_URL_CONFIG_RESPONSE = '''
    {
        "d": {
            "__type": "MyTagList.EventURLConfig",
            "oor": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "back_in_range": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "low_battery": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "motion_detected": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "door_opened": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "door_closed": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "door_open_toolong": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "update": {
                "url": "http://host_name/update",
                "verb": "POST",
                "content": "message",
                "disabled": false,
                "nat": true
            },
            "temp_toohigh": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "temp_toolow": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "temp_normal": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "light_normal": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "too_bright": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "too_dark": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "cap_normal": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "too_dry": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "too_humid": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "water_detected": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "water_dried": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "motion_timedout": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "carried_away": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            },
            "in_free_fall": {
                "url": "http://",
                "verb": null,
                "content": null,
                "disabled": true,
                "nat": false
            }
        }
    }
    '''

UPDATE_NOTIFICATION_CONFIG = {
    "url": "http://10.10.0.2/api/events/update_tags",
    "verb": "POST",
    "content": "{\"name\":\"{0}\",\"id\":{1},\"temp\": {2}, \"cap\":{3},\"lux\":{4}}",
    "disabled": False,
    "nat": True
}
