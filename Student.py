# -*- coding: utf-8 -*-

class Student(object):
    """docstring for Student"""

    def __init__(self, id, speciality_id, year):
        super(Student, self).__init__()
        self._id = id
        self._speciality_id = speciality_id
        self._year = year

    def GetId(self):
        return self._id

    def GetSpecialityId(self):
        return self._speciality_id

    def GetYear(self):
        return self._year
