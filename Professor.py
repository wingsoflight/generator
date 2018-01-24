# -*- coding: utf-8 -*-

class Professor(object):
    """docstring for Professor"""

    def __init__(self, id, name):
        super(Professor, self).__init__()
        self._id = id
        self._name = name
        self._courseClasses = []

    def GetId(self):
        return self._id

    def GetName(self):
        return self._name

    def AddCourseClass(self, courseClass):
        self._courseClasses.append(courseClass)

    def GetCourseClasses(self):
        return self._courseClasses

    def compare(self, other):
        return self._id == other._id

    def ToString(self):
        return 'Преподаватель:\n\t' + self.GetName().encode('utf-8', errors='replace')
