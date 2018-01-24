# -*- coding: utf-8 -*-

import _mssql


def generateRooms(building_id, type, room_number, capacity, floor, count):
    conn = _mssql.connect(server='212.19.138.133', user='nitu_test', password='asdQWE123', database='KazNITU_Test')
    for i in range(count):
        conn.execute_non_query(
            "INSERT INTO Edu_Rooms (BuildingID, TypeID, Title, Capacity, Floor, Active) VALUES(%d, %d, %d, %d, %d, 1)",
            (building_id, type, room_number, capacity, floor))
        room_number += 1


generateRooms(1, 2, 301, 30, 3, 90)
generateRooms(2, 2, 301, 30, 3, 30)
generateRooms(3, 2, 301, 30, 3, 30)
generateRooms(7, 2, 301, 30, 3, 30)
generateRooms(8, 2, 301, 30, 3, 30)

generateRooms(1, 3, 401, 30, 4, 90)
generateRooms(2, 3, 401, 30, 4, 30)
generateRooms(3, 3, 401, 30, 4, 30)
generateRooms(7, 3, 401, 30, 4, 30)
generateRooms(8, 3, 401, 30, 4, 30)
