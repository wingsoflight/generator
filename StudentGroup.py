# -*- coding: utf-8 -*-

class StudentGroup(object):
    """docstring for StudentGroup"""

    def __init__(self, numberOfStudents, group_number, students):
        super(StudentGroup, self).__init__()
        self._numberOfStudents = numberOfStudents
        self._group_number = group_number
        self._students = students

    def GetNumberOfStudents(self):
        return self._numberOfStudents

    def GetStudents(self):
        return self._students

    def GetGroupNumber(self):
        return self._group_number

    def ToString(self):
        return 'Количество студентов в группе:\n\t' + str(self.GetNumberOfStudents()).encode('utf-8',
                                                                                             errors='replace') + '\nФактическое количество:\n\t' + str(
            len(self._students))
