# -*- coding: utf-8 -*-
# @Author: bobur554395
# @Date:   2017-05-23 13:38:38
# @Last Modified by:   bobur554395
# @Last Modified time: 2017-06-01 14:50:38


class ConfigOptions(object):
    """docstring for ConfigOptions"""

    def __init__(self, _year, day_hours, days_num, semesterId):
        super(ConfigOptions, self).__init__()
        self.year = _year
        self.DAYS_NUM = day_hours
        self.DAY_HOURS = days_num
        self.voenka_day = None
        self.bekturova_day = None
        self.criteria_count = self.getCriteriaCount(self.year)
        self.semesterId = semesterId

    def set_voenka_day(self, day):
        self.voenka_day = day

    def get_voenka_day(self):
        return self.voenka_day

    def set_bekturova_day(self, day):
        self.bekturova_day = day

    def get_bekturova_day(self):
        return self.bekturova_day

    def getDAY_HOURS(self, year):
        return self.DAY_HOURS

    # if year in [2,3,4]:
    # 	return 14
    # elif year == 1:
    # 	return 14


    def getDAYS_NUM(self, year):
        # return self.DAYS_NUM
        if year in [1, 2, 3]:
            return 6
        elif year == 4:
            return 6

    def getCriteriaCount(self, year):
        if year == 1:
            return 12
        else:
            return 12

    def getSemesterId(self):
        return self.semesterId

    def toString(self):
        return 'year = ' + str(self.year) + '\nDAYS_NUM = ' + str(self.DAYS_NUM) + '\nDAY_HOURS = ' + str(
            self.DAY_HOURS) + '\nvoenka_day = ' + str(self.voenka_day) + '\nbekturova_day = ' + str(
            self.bekturova_day) + '\ncriteria_count = ' + str(self.criteria_count)
