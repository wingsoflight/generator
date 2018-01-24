# -*- coding: utf-8 -*-

from CourseClass import CourseClass
import random
import time
from Constants import Constants
import _mssql


class Schedule(object):
    """docstring for Schedule"""

    # DAY_HOURS = 12
    # DAYS_NUM = 5

    def __init__(self, numberOfCrossoverPoints, mutationSize, crossoverProbability, mutationProbability, config_options,
                 configuration):
        super(Schedule, self).__init__()
        self._config_options = config_options
        self._numberOfCrossoverPoints = numberOfCrossoverPoints
        self._mutationSize = mutationSize
        self._crossoverProbability = crossoverProbability
        self._mutationProbability = mutationProbability
        self._conf = configuration
        self._fitness = 0
        self._criteria_count = self._config_options.criteria_count
        self._times = self._conf.GetTimes()
        self._days = self._conf.GetDays()
        self._criteria = [False] * self._conf.GetNumberOfCourseClasses() * self._criteria_count
        self._slots = [[] for _ in xrange(
            self._config_options.getDAYS_NUM(1) * self._config_options.DAY_HOURS * self._conf.GetNumberOfRooms())]
        self._classes = {}

    def MakeNewFromPrototype(self):

        newChromosome = Schedule(10, 3, 70, 10, self._config_options, self._conf)

        courseClasses = self._conf._courseClasses
        nr = self._conf.GetNumberOfRooms()
        for courseClass in courseClasses:
            dur = courseClass.GetDuration()
            day = random.randint(0, self._config_options.getDAYS_NUM(1) - 1)
            room = random.randint(0, nr - 1)
            time = random.randint(0, self._config_options.getDAY_HOURS(1) - dur)
            pos = day * nr * self._config_options.getDAY_HOURS(1) + room * self._config_options.getDAY_HOURS(1) + time;

            for i in xrange(0, dur):
                newChromosome._slots[pos + i].append(courseClass)

            newChromosome._classes[courseClass] = pos

        newChromosome.CalculateFitness()
        return newChromosome

    def Crossover(self, parent2):
        if random.randint(0, 99) > self._crossoverProbability:
            return self

        # print 'Crossover start'
        size = len(self._classes)
        newChromosome = Schedule(10, 2, 70, 5, self._config_options, self._conf)
        cp = [False] * size

        for i in xrange(self._numberOfCrossoverPoints, 0, -1):
            while True:
                p = random.randint(0, size - 1)
                if cp[p] == False:
                    cp[p] = True
                    break
        dic1 = self._classes
        dic2 = parent2._classes

        it1 = sorted(self._classes)
        it2 = sorted(parent2._classes)

        first = random.randint(0, 1) == 0
        for k in xrange(0, size):
            if first:
                newChromosome._classes[it1[k]] = dic1[it1[k]]
                for i in xrange(0, it1[k].GetDuration()):
                    newChromosome._slots[dic1[it1[k]] + i].append(it1[k])
            else:
                newChromosome._classes[it2[k]] = dic2[it2[k]]
                for j in xrange(0, it2[k].GetDuration()):
                    newChromosome._slots[dic2[it2[k]] + j].append(it2[k])

            if cp[k]:
                first = not first

        newChromosome.CalculateFitness()

        # print 'Crossover end'
        return newChromosome

    def Mutation(self):
        if random.randint(0, 99) > self._mutationProbability:
            return

        # print 'Mutation start'

        numberOfClasses = len(self._classes)
        size = len(self._slots)
        nr = self._conf.GetNumberOfRooms()

        for i in xrange(self._mutationSize, 0, -1):
            mpos = random.randint(0, numberOfClasses - 1)
            pos1 = 0
            it1 = iter(self._classes.iteritems())
            for i in xrange(mpos, 0, -1):
                it1.next()

            n3 = it1.next()
            cc1 = n3[0]
            pos1 = n3[1]

            dur = cc1.GetDuration()
            day = random.randint(0, self._config_options.getDAYS_NUM(1) - 1)
            room = random.randint(0, nr - 1)
            time = random.randint(0, self._config_options.DAY_HOURS - dur)
            pos2 = day * nr * self._config_options.DAY_HOURS + room * self._config_options.DAY_HOURS + time;

            for i in xrange(0, dur):
                cl = self._slots[pos1 + i]
                for j in xrange(0, len(cl)):
                    if cl[j] == cc1:
                        cl.remove(cc1)
                        break

                self._slots[pos2 + i].append(cc1)

            self._classes[cc1] = pos2

        self.CalculateFitness()
        # print 'Mutation end'

    def CalculateFitness(self):
        conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER,
                              password=Constants.PASSWORD,
                              database=Constants.DATABASE)
        score = 0
        numberOfRooms = self._conf.GetNumberOfRooms()
        reservations = self._conf.GetRoomReservations()
        daySize = self._config_options.getDAY_HOURS(1) * numberOfRooms
        ci = 0

        dic = self._classes
        it = sorted(self._classes)

        for k in xrange(0, len(dic)):
            it[k].GetCourse().ResetTimes()

        for k in xrange(0, len(dic)):
            p = dic[it[k]]
            day = p / daySize
            time = p % daySize
            room = time / self._config_options.getDAY_HOURS(1) + 1
            time = time % self._config_options.getDAY_HOURS(1)
            dur = it[k].GetDuration()

            if it[k].GetName() == Constants.LECTURE_ID:
                it[k].GetCourse().SetLectureTime(day, time)

            elif it[k].GetName() == Constants.LAB_ID:
                it[k].GetCourse().SetLabTime(day, time)

            elif it[k].GetName() == Constants.PRACTICE_ID:
                it[k].GetCourse().SetSeminarTime(day, time)

        for k in xrange(0, len(dic)):
            p = dic[it[k]]
            day = p / daySize
            time = p % daySize
            room = time / self._config_options.getDAY_HOURS(1) + 1
            time = time % self._config_options.getDAY_HOURS(1)
            dur = it[k].GetDuration()

            cc = it[k]
            r = self._conf._rooms[room]

            # criteria 1

            # check for room overlapping of classes
            ro = False
            for i in xrange(0, dur):
                if len(self._slots[p + i]) > 1:
                    ro = True
                    break

            if not ro:
                conn.execute_row(Constants.ROOM_CONFLICT_QUERY, (
                    r.GetDbId(), day + 1, time + 1, (time + 1) + (2 * dur - 1),
                    self._config_options.getSemesterId()))
                for row in conn:
                    ro = True
                    break
            # on room overlaping
            if not ro:
                score += 1

            self._criteria[ci + 0] = not ro

            # criteria 2

            # does rooms suitable for course (room type)
            # self._criteria[ci + 1] = True

            self._criteria[ci + 1] = ((r.GetRoomType() == cc.GetRoomType()))  # and
            #  (r.GetSpecialCourse() == 'все' or r.GetSpecialCourse() == cc.GetCourse().GetId()))

            if self._criteria[ci + 1]:
                score += 1

            # criteria 3

            # does current room have enough seats
            # self._criteria[ci + 2] = True
            self._criteria[ci + 2] = (r.GetNumberOfSeats() >= cc.GetNumberOfSeats())
            if self._criteria[ci + 2]:
                score += 1

            # criteria 4

            po = False
            # check overlapping of classes for professors
            t = day * daySize + time
            for l in xrange(numberOfRooms, 0, -1):

                # for each hour of class
                for j in xrange(0, dur):
                    # check for overlapping with other classes at same time
                    cl = self._slots[t + j]
                    for q in xrange(0, len(cl)):
                        if cl[q] != cc:
                            if not po and cc.ProfessorOverlaps(cl[q]):
                                po = True
                            if po:
                                break
                    if po:
                        break
                if po:
                    break

                t += self._config_options.DAY_HOURS

            if not po:
                conn.execute_row(Constants.INSTRUCTOR_CONFLICT_QUERY, (
                    cc.GetProfessor().GetId(), day + 1, time + 1, (time + 1) + (2 * dur - 1),
                    self._config_options.getSemesterId()))
                for row in conn:
                    po = True
                    break

            if not po:
                score += 1

            self._criteria[ci + 3] = not po

            # criteria 5

            # Housing of room and course class
            self._criteria[ci + 4] = True
            if (cc.GetCourse().IsSpecialRoom()):
                self._criteria[ci + 4] = (r.GetHousing() == cc.GetCourse().GetHousing())

            if self._criteria[ci + 4]:
                score += 1

            # criteria 6
            # Sport time

            self._criteria[ci + 5] = True
            if cc.GetCourse().GetCode() == "AAP106" and time != 1:
                self._criteria[ci + 5] = False

            if self._criteria[ci + 5]:
                score += 1

            # criteria 7
            # English time

            self._criteria[ci + 6] = True
            if "LNG" in cc.GetCourse().GetCode():
                code = cc.GetCourse().GetCode()
                po = False
                # check overlapping of classes for student
                t = day * daySize

                for l in xrange(numberOfRooms, 0, -1):
                    for student in cc.GetGroup().GetStudents():
                        # for each hour of day
                        for j in xrange(0, self._config_options.DAY_HOURS):
                            # check for overlapping with other classes at same day
                            # print 'day ', day
                            cl = self._slots[t + j]
                            for q in xrange(0, len(cl)):
                                if cl[q].GetId() != cc.GetId() and cl[q].GetNumber() != cc.GetNumber() and code == cl[
                                    q].GetCourse().GetCode():
                                    if not po and student in cl[q].GetGroup().GetStudents():
                                        # print 'Student: ', student.GetId(), '  Current: ', cc.GetId(), '   New: ', cl[q].GetId()
                                        po = True
                                        break
                                    if po:
                                        break
                            if po:
                                break
                        if po:
                            break
                    if po:
                        break

                    t += self._config_options.DAY_HOURS

                self._criteria[ci + 6] = not po

            if self._criteria[ci + 6]:
                score += 1

            # if (cc.GetCourse().GetCode() == "LNG1051" and (time != 3 or day not in [0, 2, 4])) or (
            #                 cc.GetCourse().GetCode() == "LNG1052" and (time != 5 or day not in [0, 2, 4])):
            #     self._criteria[ci + 6] = False
            #
            # if self._criteria[ci + 6]:
            #     score += 1

            # criteria 8
            # order of classes Lecture -> Seminar -> Lab
            self._criteria[ci + 7] = True
            if ((cc.GetCourse().GetLectureDay() > -1 and cc.GetCourse().GetLabDay() > -1 and (
                            cc.GetCourse().GetLectureDay() > cc.GetCourse().GetLabDay() or (
                                    cc.GetCourse().GetLectureDay() == cc.GetCourse().GetLabDay() and cc.GetCourse().GetLectureTime() >= cc.GetCourse().GetLabTime())))
                or (cc.GetCourse().GetSeminarDay() > -1 and cc.GetCourse().GetLabDay() > -1 and (
                                cc.GetCourse().GetLabDay() > cc.GetCourse().GetSeminarDay() or (
                                        cc.GetCourse().GetLabDay() == cc.GetCourse().GetSeminarDay() and cc.GetCourse().GetLabTime() >= cc.GetCourse().GetSeminarTime())))
                or (cc.GetCourse().GetSeminarDay() > -1 and cc.GetCourse().GetLectureDay() > -1 and (
                                cc.GetCourse().GetLectureDay() > cc.GetCourse().GetSeminarDay() or (
                                        cc.GetCourse().GetLectureDay() == cc.GetCourse().GetSeminarDay() and cc.GetCourse().GetLectureTime() >= cc.GetCourse().GetSeminarTime())))):
                self._criteria[ci + 7] = False

            if self._criteria[ci + 7]:
                score += 1

            # criteria 9
            po = False
            # check in a row classes for professors
            t = day * daySize + time + dur
            for l in xrange(numberOfRooms, 0, -1):

                # for each hour of class
                # check for overlapping with other classes at same time
                if len(self._slots) > t:
                    cl = self._slots[t]
                    for q in xrange(0, len(cl)):
                        if cl[q] != cc:
                            if not po and cc.ProfessorOverlaps(cl[q]):
                                if cc.GetCourse().GetHousing() != cl[q].GetCourse().GetHousing():
                                    po = True

                            if po:
                                break
                    if po:
                        break

                    t += self._config_options.DAY_HOURS

            if not po:
                score += 1
            self._criteria[ci + 8] = not po
            # score += 1
            # self._criteria[ci + 8] = True



            # criteria 10
            self._criteria[ci + 9] = True
            for option in self._conf.GetAdOptions():
                for student in cc.GetGroup().GetStudents():
                    if cc.GetCourse().GetId() != option.GetCourseId() and student.GetSpecialityId() == option.GetSpecialityId() and day == option.GetDayOfWeekId():
                        self._criteria[ci + 9] = False
                        break
                if not self._criteria[ci + 9]:
                    break
            if self._criteria[ci + 9]:
                score += 1

            # criteria 11
            self._criteria[ci + 10] = True
            reservations = self._conf.GetRoomReservations()
            id = self._conf.GetRooms()[room].GetId()
            if id in reservations:
                for reservation in reservations[id]:
                    if reservation.GetDayId() == day and (
                                (reservation.GetStartId() <= time and reservation.GetEndId() > time) or (
                                            reservation.GetStartId() < time + dur and reservation.GetEndId() > time + dur)):
                        self._criteria[ci + 10] = False

            if self._criteria[ci + 10]:
                score += 1
            # print 'SCORE: ', score


            # criteria 12
            # Student Overlaps

            po = False
            # check overlapping of classes for student
            t = day * daySize + time

            for l in xrange(numberOfRooms, 0, -1):
                for student in cc.GetGroup().GetStudents():
                    # for each hour of day
                    for j in xrange(0, dur):
                        # check for overlapping with other classes at same day
                        # print 'day ', day
                        cl = self._slots[t + j]
                        for q in xrange(0, len(cl)):
                            if cl[q].GetId() != cc.GetId() and cl[q].GetNumber() != cc.GetNumber():
                                if not po and student in cl[q].GetGroup().GetStudents():
                                    # print 'Student: ', student.GetId(), '  Current: ', cc.GetId(), '   New: ', cl[q].GetId()
                                    po = True
                                    break
                                if po:
                                    break
                        if po:
                            break
                    if po:
                        break
                if po:
                    break

                t += self._config_options.DAY_HOURS

            if not po:
                score += 1
            self._criteria[ci + 11] = not po

            ci += self._criteria_count

        # print 'CourseClasses: ', self._conf.GetNumberOfCourseClasses()
        # print 'SCORE: ', score
        # print 'Criteria Count: ', self._criteria_count
        self._fitness = float(score) / (self._conf.GetNumberOfCourseClasses() * self._criteria_count)
        # print 'FITNESS: ', self._fitness
        conn.close()

    def GetFitness(self):
        return self._fitness

    def GetClasses(self):
        return self._classes

    def GetCriteria(self):
        return self._criteria

    def GetSlots(self):
        return self._slots

    def Where(self, course):
        pass

# s = Schedule()
# ss = s.MakeNewFromPrototype()
# print ss._fitness
