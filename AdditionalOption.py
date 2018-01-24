# -*- coding: utf-8 -*-

class AdditionalOption(object):
    def __init__(self, year_of_admission, speciality_id, course_id, building_id, day_of_week_id):
        super(AdditionalOption, self).__init__()
        self._year_of_admission = year_of_admission
        self._speciality_id = speciality_id
        self._course_id = course_id
        self._building_id = building_id
        self._day_of_week_id = day_of_week_id

    def GetYearOfAdmission(self):
        return self._year_of_admission

    def GetSpecialityId(self):
        return self._speciality_id

    def GetCourseId(self):
        return self._course_id

    def GetBuildingId(self):
        return self._building_id

    def GetDayOfWeekId(self):
        return self._day_of_week_id
