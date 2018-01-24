# -*- coding: utf-8 -*-


class Configuration(object):
    """docstring for Configuration"""

    def __init__(self, rooms, professors, courses, courseClasses, reservations, ad_options, times, days):
        super(Configuration, self).__init__()
        self._rooms = rooms
        self._professors = professors
        self._courses = courses
        self._courseClasses = courseClasses
        self._reservations = reservations
        self._ad_options = ad_options
        self._times = times
        self._days = days
        # self.readRooms()
        # self.readProfessors()
        # self.readCourses()
        # self.readStudentGroups()

    def GetNumberOfRooms(self):
        return len(self._rooms)

    def GetNumberOfCourseClasses(self):
        return len(self._courseClasses)

    def GetRoomReservations(self):
        return self._reservations

    def GetAdOptions(self):
        return self._ad_options

    def GetRooms(self):
        return self._rooms

    def GetTimes(self):
        return self._times

    def GetDays(self):
        return self._days

# c = Configuration()

# print c.
