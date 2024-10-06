import sqlite3
import json
def db(data):
    conn = sqlite3.connect('info.db')

    cursor = conn.cursor()

    stopTable = []

    cursor.execute('''
        create table if not exists stopTable (
            stop_id integer primary key autoincrement,
            latitude real not null,
            longitude real not null,
            distance real not null,
            time real not null
        )
    ''')

    ##update here to take in the json
    if 'apple' in data and 'coords' in data['apple'] and 'distanceMeters' in data['apple']:
        for coord in data['apple']['coords']:
            stopTable.append((coord['lat'], coord['lng'], data['apple']['distanceMeters'],data['apple']['timeSeconds']))

    if 'google' in data and 'coords' in data['google'] and 'distanceMeters' in data['google']:
        for coord in data['google']['coords']:
            stopTable.append((coord['lat'], coord['lng'], data['google']['distanceMeters'],data['google']['timeSeconds']))

    if 'waze' in data and 'coords' in data['waze'] and 'distanceMeters' in data['waze']:
        for coord in data['waze']['coords']:
            stopTable.append((coord['lat'], coord['lng'], data['waze']['distanceMeters'],data['waze']['timeSeconds']))

    # Insert the latitude, longitude, and distance values into the database
    cursor.executemany('''
        insert into stopTable (latitude, longitude, distance, time) values (?, ?, ?, ?)
    ''', stopTable)

    conn.commit()

    conn.close()