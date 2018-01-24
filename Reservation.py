# -*- coding: utf-8 -*-

class Reservation(object):
    """docstring for Room"""

    def __init__(self, room_id, day_id, start_id, end_id):
        super(Reservation, self).__init__()
        self._room_id = room_id
        self._day_id = day_id
        self._start_id = start_id
        self._end_id = end_id

    def GetRoomId(self):
        return self._room_id

    def GetDayId(self):
        return self._day_id

    def GetStartId(self):
        return self._start_id

    def GetEndId(self):
        return self._end_id
