# -*- coding: utf-8 -*-

class Course(object):
    """docstring for Course"""

    def __init__(self, id, code, name, is_special_room, housing, speciality, lectures, labs, practices):
        super(Course, self).__init__()
        self._id = id
        self._code = code
        self._name = name
        self._is_special_room = is_special_room
        self._housing = housing
        self._speciality = speciality
        self._lectures = lectures
        self._labs = labs
        self._practices = practices
        self._lecture_time = -1
        self._lab_time = -1
        self._seminar_time = -1
        self._lecture_day = -1
        self._lab_day = -1
        self._seminar_day = -1

    def GetId(self):
        return self._id

    def GetCode(self):
        return self._code

    def GetName(self):
        return self._name

    def IsSpecialRoom(self):
        return self._is_special_room

    def IsSpecialRoomName(self, ok):
        return "да" if ok else "нет"

    def GetHousing(self):
        return self._housing

    def GetSpeciality(self):
        return self._speciality

    def GetLectures(self):
        return self._lectures

    def GetLabs(self):
        return self._labs

    def GetPractices(self):
        return self._practices

    def GetLectureTime(self):
        return self._lecture_time

    def SetLectureTime(self, day, time):
        if (self._lecture_day == -1 or self._lecture_time == -1) or day < self._lecture_day or (
                day == self._lecture_day and time < self._lecture_time):
            self.SetLectureDay(day)
            self._lecture_time = time

    def GetLabTime(self):
        return self._lab_time

    def SetLabTime(self, day, time):
        if (self._lab_day == -1 or self._lab_time == -1) or day < self._lab_day or (
                day == self._lab_day and time < self._lab_time):
            self.SetLabDay(day)
            self._lab_time = time

    def GetSeminarTime(self):
        return self._seminar_time

    def SetSeminarTime(self, day, time):
        if (self._seminar_day == -1 or self._seminar_time == -1) or day < self._seminar_day or (
                day == self._seminar_day and time < self._seminar_time):
            self.SetSeminarDay(day)
            self._seminar_time = time

    def GetLectureDay(self):
        return self._lecture_day

    def SetLectureDay(self, day):
        self._lecture_day = day

    def GetLabDay(self):
        return self._lab_day

    def SetLabDay(self, day):
        self._lab_day = day

    def GetSeminarDay(self):
        return self._seminar_day

    def SetSeminarDay(self, day):
        self._seminar_day = day

    def ResetTimes(self):
        self._lecture_time = -1
        self._lab_time = -1
        self._seminar_time = -1
        self._lecture_day = -1
        self._lab_day = -1
        self._seminar_day = -1

    def ToString(self):
        return 'Предмет:\n\tНаименование: ' + self.GetName().encode('utf-8',
                                                                    errors='replace') + '\n\tСпец.лаборатория: ' + self.IsSpecialRoomName(
            self.IsSpecialRoom()) + '\n\tКорпус: ' + str(self.GetHousing()).encode('utf-8',
                                                                                   errors='replace') + '\n\tСпециальность: ' + str(
            self.GetSpeciality())
