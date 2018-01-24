# -*- coding: utf-8 -*-

from Professor import Professor
from StudentGroup import StudentGroup
from Course import Course


class CourseClass(object):
    """docstring for CourseClass"""

    def __init__(self, id, name, class_type, professor, course, group, room_type, duration, number):
        super(CourseClass, self).__init__()
        self._id = id
        self._name = name
        self._class_type = class_type
        self._professor = professor
        self._course = course
        self._group = group
        self._room_type = room_type
        self._duration = duration
        self._number = number
        self.TYPES = {
            1: "Лекционный зал",
            2: "Учебная аудитория",
            3: "Компьютерный класс"
        }
        self._professor.AddCourseClass(self)

    def GetId(self):
        return self._id

    def GetNumber(self):
        return self._number

    def ProfessorOverlaps(self, other_course):
        return self._professor == other_course._professor

    def GroupsOverlap(self, other_course):
        return self._group.compare(other_course._group)

    def GetProfessor(self):
        return self._professor

    def GetName(self):
        return self._name

    def GetClassType(self):
        return self._class_type

    def GetCourse(self):
        return self._course

    def GetGroup(self):
        return self._group

    def SetGroup(self, group):
        self._group = group

    def GetRoomTypeName(self):
        return self.TYPES[self._room_type]

    def GetRoomType(self):
        return self._room_type

    def GetDuration(self):
        return self._duration

    def GetNumberOfSeats(self):
        return self._group._numberOfStudents

    def ToString(self):
        return self.GetCourse().ToString() + '\n' + self.GetProfessor().ToString() + '\nТип урока:\n\t' + str(
            self.GetName()).encode('utf-8',
                                   errors='replace') + '\n' + self.GetGroup().ToString() + '\nПродолжительность урока:\n\t' + str(
            self.GetDuration()).encode('utf-8', errors='replace') + '\nТип кабинета:\n\t' + str(self.GetRoomTypeName())

# p = Professor(1, "professor1")
# c = Course(1, "course1")
# g = StudentGroup(1, "group1", 200)
# cc = CourseClass(p, c, g, True, 2)

# print g.GetCourseClasses()[0].GetCourse().GetName()
