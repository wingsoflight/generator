# -*- coding: utf-8 -*-

class Day(object):
    """docstring for Room"""

    def __init__(self, id, title):
        super(Day, self).__init__()
        self._id = id
        self._title = title

    def GetId(self):
        return self._id

    def GetTitle(self):
        return self._title
