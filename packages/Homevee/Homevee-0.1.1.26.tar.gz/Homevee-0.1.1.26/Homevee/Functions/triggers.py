#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Utils.Database import Database


def add_trigger(user, location, id, db: Database = None):
    if db is None:
        db = Database()
    return

def get_triggers(user, room, db: Database = None):
    if db is None:
        db = Database()
    if not user.has_permission(room):
        return {'result': 'nopermission'}

    triggers = []

    results = db.select_all("SELECT * FROM MQTT_TRIGGERS WHERE LOCATION = :location", {'location': room})

    for item in results:
        triggers.append({'name': item['NAME'], 'id': item['ID'], 'type': 'MQTT-Trigger', 'icon': item['ICON']})

    return {'triggers': triggers}