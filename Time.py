# -*- coding: utf-8 -*-

class Time(object):
    """docstring for Room"""

    def __init__(self, id, title, end_of_interval):
        super(Time, self).__init__()
        self._id = id
        self._title = title
        self._end_of_interval = end_of_interval

    def GetId(self):
        return self._id

    def GetTitle(self):
        return self._title

    def GetEndOfInterval(self):
        return self._end_of_interval
