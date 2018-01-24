# -*- coding: utf-8 -*-

class Room(object):
    """docstring for Room"""

    def __init__(self, id, db_id, housing, roomNumber, numberOfSeats, room_type, is_special_room, special_course):
        super(Room, self).__init__()
        self._id = id
        self._db_id = db_id
        self._housing = housing
        self._roomNumber = roomNumber
        self._numberOfSeats = numberOfSeats
        self._room_type = room_type
        self._is_special_room = is_special_room
        self._special_course = special_course
        self.TYPES = {
            1: "Лекционный зал",
            2: "Учебная аудитория",
            3: "Компьютерный класс"
        }

    def GetId(self):
        return self._id

    def GetDbId(self):
        return self._db_id

    def GetRoomNumber(self):
        return self._roomNumber

    def GetRoomType(self):
        return self._room_type
        # return self.TYPES[self._room_type]

    def GetHousing(self):
        return self._housing

    def GetNumberOfSeats(self):
        return self._numberOfSeats

    def GetSpecialCourse(self):
        return self._special_course

    def IsSpecialRoom(self):
        return self._is_special_room

    def ToString(self):
        return 'Информация о кабинете:\n\tКорпус: ' + str(
            self.GetHousing()) + '\n\tНомер кабинета: ' + self.GetRoomNumber().encode('utf-8',
                                                                                      errors='replace') + '\n\tТип кабинета: ' + str(
            self.GetRoomType()) + '\n\tВместимость: ' + str(self.GetNumberOfSeats()) + '\n\tКабинет для: ' + str(
            self.GetSpecialCourse())
