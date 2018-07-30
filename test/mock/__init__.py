"""mocks live here."""

ALS_PRO = {
    "name": "Kitchen",
    "uuid": "fake-1111-2222-4444-111111111111",
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
                "__type": "MyTagList.TagManagerTag",
                "mac": "000011112222",
                "tags": [
                    {
                        "LBTh": 2.55,
                        "OutOfRange": false,
                        "__type": "MyTagList.Tag",
                        "alive": true,
                        "az2": 0,
                        "batteryRemaining": 0.39,
                        "batteryVolt": 2.6214669823743697,
                        "beepDurationDefault": 15,
                        "beeping": false,
                        "cap": 42.8128662109375,
                        "capCalOffset": 0,
                        "capEventState": 1,
                        "capRaw": 0,
                        "comment": "",
                        "ds18": false,
                        "enLBN": true,
                        "eventState": 0,
                        "freqCalApplied": 5721,
                        "freqOffset": -1759,
                        "image_md5": "+d1D4tMIvNeDQOxcIzXdig==",
                        "lastComm": 131773844515317582,
                        "lightEventState": 0,
                        "lit": false,
                        "lux": 0,
                        "migrationPending": false,
                        "name": "House",
                        "notificationJS": "",
                        "oorGrace": 2,
                        "playback": null,
                        "postBackInterval": 1800,
                        "rev": 14,
                        "reviveEvery": 255,
                        "rssiMode": true,
                        "shorted": false,
                        "signaldBm": -72,
                        "slaveId": 0,
                        "tagType": 13,
                        "tempCalOffset": 0,
                        "tempEventState": 1,
                        "temperature": -22.5040283203125,
                        "thermostat": null,
                        "txpwr": 32,
                        "uuid": "fake-1111-2222-3333-111111111111",
                        "v2flag": 16,
                        "version1": 2
                    },
                    {
                        "LBTh": 2.55,
                        "OutOfRange": false,
                        "__type": "MyTagList.Tag",
                        "alive": true,
                        "az2": 0,
                        "batteryRemaining": 0.84,
                        "batteryVolt": 2.864808380010022,
                        "beepDurationDefault": 5,
                        "beeping": false,
                        "cap": 18.58953857421875,
                        "capCalOffset": 0,
                        "capEventState": 0,
                        "capRaw": 0,
                        "comment": "",
                        "ds18": false,
                        "enLBN": true,
                        "eventState": 0,
                        "freqCalApplied": 410,
                        "freqOffset": 2144,
                        "image_md5": "OLldHRpVn/YyVetG5vPyaA==",
                        "lastComm": 131773836260003295,
                        "lightEventState": 0,
                        "lit": false,
                        "lux": 0,
                        "migrationPending": false,
                        "name": "Refrigerator",
                        "notificationJS": "",
                        "oorGrace": 2,
                        "playback": null,
                        "postBackInterval": 1800,
                        "rev": 14,
                        "reviveEvery": 255,
                        "rssiMode": true,
                        "shorted": false,
                        "signaldBm": -78,
                        "slaveId": 3,
                        "tagType": 13,
                        "tempCalOffset": 0,
                        "tempEventState": 1,
                        "temperature": 5.231074333190918,
                        "thermostat": null,
                        "txpwr": 21,
                        "uuid": "fake-1111-2222-3333-111111111111",
                        "v2flag": 16,
                        "version1": 2
                    },
                    
                ]
            },
            {
                "__type": "MyTagList.TagManagerTag",
                "mac": "333344445555",
                "tags": [
                    {
                        "LBTh": 2.55,
                        "OutOfRange": false,
                        "__type": "MyTagList.Tag",
                        "alive": true,
                        "az2": 0,
                        "batteryRemaining": 0.31,
                        "batteryVolt": 2.746555099856411,
                        "beepDurationDefault": 15,
                        "beeping": false,
                        "cap": 4.284423828125,
                        "capCalOffset": 0,
                        "capEventState": 0,
                        "capRaw": 0,
                        "comment": "",
                        "ds18": false,
                        "enLBN": true,
                        "eventState": 0,
                        "freqCalApplied": 1158,
                        "freqOffset": 605,
                        "image_md5": null,
                        "lastComm": 131773845471091737,
                        "lightEventState": 0,
                        "lit": false,
                        "lux": 0,
                        "migrationPending": false,
                        "name": "Shop",
                        "notificationJS": "",
                        "oorGrace": 2,
                        "playback": null,
                        "postBackInterval": 600,
                        "rev": 14,
                        "reviveEvery": 255,
                        "rssiMode": true,
                        "shorted": false,
                        "signaldBm": -76,
                        "slaveId": 0,
                        "tagType": 13,
                        "tempCalOffset": 0,
                        "tempEventState": 0,
                        "temperature": 4.008413314819336,
                        "thermostat": null,
                        "txpwr": 162,
                        "uuid": "fake-1111-2222-3333-111111111111",
                        "v2flag": 26,
                        "version1": 2
                    },
                    {
                        "LBTh": 2.55,
                        "OutOfRange": false,
                        "__type": "MyTagList.Tag",
                        "alive": true,
                        "az2": 0,
                        "batteryRemaining": 0.56,
                        "batteryVolt": 2.67266826148845,
                        "beepDurationDefault": 15,
                        "beeping": false,
                        "cap": 47.9093017578125,
                        "capCalOffset": 0,
                        "capEventState": 0,
                        "capRaw": 0,
                        "comment": "",
                        "ds18": false,
                        "enLBN": true,
                        "eventState": 0,
                        "freqCalApplied": 3001,
                        "freqOffset": -31,
                        "image_md5": null,
                        "lastComm": 131773841252033008,
                        "lightEventState": 0,
                        "lit": false,
                        "lux": 0,
                        "migrationPending": false,
                        "name": "Office",
                        "notificationJS": "beep_once(false)",
                        "oorGrace": 2,
                        "playback": null,
                        "postBackInterval": 600,
                        "rev": 14,
                        "reviveEvery": 24,
                        "rssiMode": true,
                        "shorted": false,
                        "signaldBm": -82,
                        "slaveId": 1,
                        "tagType": 13,
                        "tempCalOffset": 0,
                        "tempEventState": 1,
                        "temperature": -18.70734405517578,
                        "thermostat": null,
                        "txpwr": 19,
                        "uuid": "fake-1111-2222-3333-111111111111",
                        "v2flag": 26,
                        "version1": 2
                    },
                ]
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
