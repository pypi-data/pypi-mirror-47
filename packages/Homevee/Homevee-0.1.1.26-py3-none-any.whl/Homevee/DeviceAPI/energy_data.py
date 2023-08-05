#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time

from Homevee.Item.Room import Room
from Homevee.Item.Status import *
from Homevee.Utils.Database import Database
from Homevee.Utils.DeviceTypes import *


def get_power_usage_devices(username, room, db: Database = None):
    if db is None:
        db = Database()
    devices = []

    for item in get_energy_device_data(username, room, db):
        try:
            if item['value'] is not None:
                item['value'] = str(round(item['value'], 2)) + " kWh"
            else:
                item['value'] = "N/A"
        except:
            item['value'] = "N/A"
        devices.append(item)

    return devices

def get_energy_device_data(user, room, db: Database = None):
    if db is None:
        db = Database()
    devices = []

    if not user.has_permission(room):
        return {'result': 'nopermission'}

    # Z-Wave Stromzähler
    results = db.select_all("SELECT * FROM ZWAVE_POWER_METER WHERE ROOM_ID = :room", {'room': room})
    for item in results:
        try:
            value = float(item['VALUE'])
        except:
            value = "N/A"
        devices.append({'name': item['DEVICE_NAME'], 'id': item['DEVICE_ID'], 'devicetype': ZWAVE_POWER_METER,
                        'icon': item['ICON'], 'value': value, 'location': room})
    return devices

def get_current_power_usage(username, db: Database = None):
    if db is None:
        db = Database()
    devices = []

    rooms = Room.load_all(db)

    for room in rooms:
        devices.extend(get_energy_device_data(username, room.id, db))

    return devices

def get_current_room_power_usage(username, db: Database = None):
    if db is None:
        db = Database()
    rooms = {}

    for room in Room.load_all(db):
        usage = 0
        for device in get_energy_device_data(username, room.id, db):
            if device['value'] is not None:
                usage += device['value']

        rooms[str(room.id)] = {'usage': usage, 'devices': get_energy_device_data(username, room.id, db)}

    return rooms

def get_current_device_power_usage(username, room, type, id, db: Database = None):
    if db is None:
        db = Database()
    devices = get_power_usage_devices(username, room, db)

    for device in devices:
        if device['devicetype'] == type and device['id'] == id:
            return device['VALUE']
    return None

def get_energy_data(username, room, devicetype, deviceid, von, bis, db: Database = None):
    if db is None:
        db = Database()
    von = datetime.datetime.strptime(von, '%d.%m.%Y')
    bis = datetime.datetime.strptime(bis, '%d.%m.%Y')

    if((room is None or room == "")
            and (devicetype is None or devicetype == "")
            and (deviceid is None or deviceid == "")):
        with db:
            room_data = get_current_room_power_usage(username, db)

            rooms_sum = 0
            for room_item in room_data:
                rooms_sum += room_data[room_item]['usage']

            data = {}

            result = db.select_one("SELECT SUM(POWER_USAGE) AS POWER_USAGE FROM ENERGY_DATA WHERE DATE >= :von AND DATE <= :bis",
                        {'von': von, 'bis': bis})
            data['totalusage'] = result['POWER_USAGE']+rooms_sum
            data['cost'] = get_power_cost(username, db)

            percentage = []
            results = db.select_all("SELECT ROOMS.NAME, SUM(POWER_USAGE) AS USAGE, ROOM_ID FROM ROOM_ENERGY_DATA, ROOMS WHERE ROOM_ID = ROOMS.LOCATION AND DATE >= :von AND DATE <= :bis GROUP BY ROOM_ID",
                        {'von': von, 'bis': bis})

            for item in results:
                energy_item = {'type': '', 'id': '', 'location': item['ROOM_ID'],
                                    'name': item['NAME'], 'usage': float(item['USAGE'])+room_data[str(item['ROOM_ID'])]['usage']}
                percentage.append(energy_item)

            data['usagepercentage'] = percentage

            data['usagecourse'] = get_energy_course(username, room, von, bis, db)
            data['usagecourse'].append({'date': time.strftime('%d.%m.%Y'), 'usage': rooms_sum})

            return {'energydata': data}
    elif(type is not None and type != '' and deviceid is not None and deviceid != '' and room is not None and room != ''):
        return get_device_energy_data(username, room, devicetype, deviceid, von, bis, db)
    else:
        return get_room_energy_data(username, room, von, bis, db)

def get_room_energy_data(username, room, von, bis, db: Database = None):
    if db is None:
        db = Database()
    data = {}
    room_data = get_current_room_power_usage(username, db)[room]['devices']
    room_data_dict = {}
    room_total_usage = 0
    for item in room_data:
        room_total_usage += item['value']
        room_data_dict[str(item['id'])+str(item['devicetype'])] = item['value']

    result = db.select_all("SELECT SUM(POWER_USAGE) AS POWER_USAGE FROM ROOM_ENERGY_DATA WHERE ROOM_ID = :room AND DATE >= :von AND DATE <= :bis",
                {'room': room, 'von': von, 'bis': bis})

    power_usage = 0

    if(result['POWER_USAGE'] is not None):
        power_usage = result['POWER_USAGE']

    data['totalusage'] = float(power_usage)+room_total_usage
    data['cost'] = get_power_cost(username, db)

    percentage = []

    device_types = []

    device_types.append("SELECT SUM(POWER_USAGE) AS POWER_USAGE, DEVICE_NAME, DEVICE_TYPE, DEVICE_ENERGY_DATA.DEVICE_ID FROM DEVICE_ENERGY_DATA, ZWAVE_POWER_METER WHERE LOCATION = ROOM_ID AND DEVICE_TYPE = \""+ZWAVE_POWER_METER+"\" AND LOCATION = :room AND DATE >= :von AND DATE <= :bis GROUP BY DEVICE_NAME")

    #device_types.append("SELECT SUM(POWER_USAGE) AS POWER_USAGE, DEVICE_NAME, DEVICE_TYPE, DEVICE_ENERGY_DATA.DEVICE_ID	FROM DEVICE_ENERGY_DATA, DIY_POWER_METER WHERE LOCATION = ROOM_ID AND DEVICE_TYPE = "+DIY+" AND LOCATION = :room AND DATE >= :von AND DATE <= :bis GROUP BY DEVICE_NAME")

    #print("SELECT SUM(POWER_USAGE) AS POWER_USAGE, DEVICE_NAME, DEVICE_TYPE, DEVICE_ENERGY_DATA.DEVICE_ID FROM DEVICE_ENERGY_DATA, ZWAVE_POWER_METER WHERE LOCATION = ROOM_ID AND DEVICE_TYPE = \""+ZWAVE_POWER_METER+"\" AND LOCATION = \""+str(room)+"\" AND DATE >= \""+str(von.strftime('%Y-%m-%d'))+"\" AND DATE <= \""+str(bis.strftime('%Y-%m-%d'))+"\" GROUP BY DEVICE_NAME")

    for device_type in device_types:
        results = db.select_all(device_type, {'room': room, 'von': von, 'bis': bis})

        for item in results:
            #print(item)

            current_item_value = room_data_dict[str(item['DEVICE_ID'])+str(item['DEVICE_TYPE'])]

            percentage.append({'type': item['DEVICE_TYPE'],'id': item['DEVICE_ID'],
                               'location': room, 'name': item['DEVICE_NAME'], 'usage': float(item['POWER_USAGE'])+current_item_value})

    data['usagepercentage'] = percentage

    data['usagecourse'] = get_energy_course(username, room, von, bis, db)
    data['usagecourse'].append({'date': time.strftime('%d.%m.%Y'), 'usage': room_total_usage})

    return {'energydata': data}

def get_device_energy_data(username, room , devicetype, deviceid, von, bis, db: Database = None):
    if db is None:
        db = Database()
    data = {}
    result = db.select_all("SELECT SUM(POWER_USAGE) AS POWER_USAGE FROM DEVICE_ENERGY_DATA WHERE DEVICE_TYPE = :type AND DEVICE_ID = :id AND DATE >= :von AND DATE <= :bis",
                {'type': devicetype, 'id': deviceid, 'von':von, 'bis': bis})

    data['totalusage'] = float(result['POWER_USAGE'])
    data['cost'] = get_power_cost(username, db)

    data['usagcourse'] = get_device_energy_course(username, room, devicetype, deviceid, von, bis, db)

    return {'energydata': data}

def get_device_energy_course(username, room, type, id, von, bis, db: Database = None):
    if db is None:
        db = Database()
    course = []

    results = db.select_all("SELECT POWER_USAGE, strftime(\"%d.%m.%Y\", DATE) as DATETIME FROM DEVICE_ENERGY_DATA WHERE DEVICE_TYPE = :type AND DEVICE_ID = :id AND DATE >= :von AND DATE <= :bis ORDER BY DATE ASC",
        {'type': type, 'id': id, 'von': von, 'bis': bis})

    for item in results:
        course.append({'date': item['DATETIME'], 'usage': item['POWER_USAGE']})

    return course

def get_energy_course(username, room, von, bis, db: Database = None):
    if db is None:
        db = Database()
    course = []

    if (room is not None and room != ""):
        results = db.select_all("""SELECT POWER_USAGE, strftime(\"%d.%m.%Y\", DATE) as DATETIME FROM ROOM_ENERGY_DATA 
        WHERE ROOM_ID = :room AND DATE >= :von AND DATE <= :bis ORDER BY DATE ASC""",
                                      {'room': room, 'von': von, 'bis': bis})
    else:
        results = db.select_all("""SELECT SUM(POWER_USAGE) as POWER_USAGE, strftime(\"%d.%m.%Y\", DATE) as DATETIME 
        FROM ROOM_ENERGY_DATA WHERE DATE >= :von AND DATE <= :bis GROUP BY DATE ORDER BY DATE ASC""",
                                      {'von': von, 'bis': bis})

    for item in results:
        course.append({'date': item['DATETIME'], 'usage': item['POWER_USAGE']})

    return course

def set_power_cost(username, cost, db: Database = None):
    if db is None:
        db = Database()
    #TODO set power cost

    return Status(type=STATUS_OK).get_dict()

def get_power_cost(username, db: Database = None):
    if db is None:
        db = Database()
    power_cost = 0.3

    return round(power_cost, 2)