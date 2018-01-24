# -*- coding: utf-8 -*-

from Schedule import Schedule
from ConfigOptions import ConfigOptions
from Configuration import Configuration
from DatabaseHelper import DatabaseHelper
import random
import time
from termcolor import colored as cd
import _mssql
import time
import datetime
from Constants import Constants
import threading


class Algorithm(object):
    """docstring for Algorithm"""

    def __init__(self, numberOfChromosomes, replaceByGeneration, trackBest, prototype, scheduleInfoId):
        super(Algorithm, self).__init__()
        self.conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                   database=Constants.DATABASE)
        self._scheduleInfoId = scheduleInfoId
        self._chromosomes = []
        self._bestFlags = []
        self._bestChromosomes = []
        self._currentBestSize = 0
        self._replaceByGeneration = replaceByGeneration
        self._prototype = prototype
        self._currentGeneration = 0
        self.thread = threading.currentThread()

        if numberOfChromosomes < 2:
            numberOfChromosomes = 2

        if trackBest < 1:
            trackBest = 1

        if self._replaceByGeneration < 1:
            self._replaceByGeneration = 1
        elif self._replaceByGeneration > numberOfChromosomes - trackBest:
            self._replaceByGeneration = numberOfChromosomes - trackBest

        self._chromosomes = [None] * numberOfChromosomes
        self._bestFlags = [False] * numberOfChromosomes

        self._bestChromosomes = [None] * trackBest

    def Start(self):

        if self._prototype == False:
            return

        self.ClearBest()

        t0 = time.time()
        for it in xrange(0, len(self._chromosomes)):
            self._chromosomes[it] = self._prototype.MakeNewFromPrototype()
            self.AddToBest(it)

        self._currentGeneration = 0
        while True:
            best = self.GetBestChromosome()
            # self.parinTable(best)
            # return
            if best.GetFitness() >= 1:
                self.conn.execute_non_query(
                    'UPDATE Edu_Semesters_ScheduleInfo SET StatusID = 4 WHERE ID = %d',
                    self._scheduleInfoId)
                self.Stop()
                break
            elif getattr(self.thread, "isStopped", False):
                self.conn.execute_non_query(
                    'UPDATE Edu_Semesters_ScheduleInfo SET StatusID = 5  WHERE ID = %d',
                    self._scheduleInfoId)
                self.Stop()
                break
            offspring = [None] * self._replaceByGeneration
            for k in xrange(0, self._replaceByGeneration):
                p1 = self._chromosomes[random.randint(0, len(self._chromosomes) - 1)]
                p2 = self._chromosomes[random.randint(0, len(self._chromosomes) - 1)]
                offspring[k] = p1.Crossover(p2)
                offspring[k].Mutation()

            for j in xrange(0, self._replaceByGeneration):
                ci = random.randint(0, len(self._chromosomes) - 1)
                while self.IsInBest(ci):
                    ci = random.randint(0, len(self._chromosomes) - 1)

                self._chromosomes[ci] = offspring[j]
                self.AddToBest(ci)

            # if best != self.GetBestChromosome():
            #   print 'best updated'
            #   print [ self._chromosomes[i].GetFitness() for i in self._bestChromosomes]
            #   print best.GetFitness(), self.GetBestChromosome().GetFitness()
            #   time.sleep(2)
            print '\n'
            print "generation = ", self._currentGeneration, " current generation fitness = ", best.GetFitness()
            print [self._chromosomes[i].GetFitness() for i in self._bestChromosomes]
            print '\n'

            self._currentGeneration += 1


    def Stop(self):
        # self._isStopped = False
        best = self.GetBestChromosome()

        print '\n' * 2
        # self.parinTable(best)
        print '*' * 100
        print "FOUND BEST SOLUTON at fitness = ", best.GetFitness()
        print '*' * 100
        print '\n' * 2
        print '*' * 100
        minute = int((time.time() - self.t0) / 60)
        sec = int((time.time() - self.t0) % 60)
        print "Execution time: %im %is" % (minute, sec)
        print '*' * 100
        print '\n' * 2
        self.saveSchedule(best)
        




    def AddToBest(self, chromosomeIndex):
        if ((self._currentBestSize == len(self._bestChromosomes)
             and self._chromosomes[self._bestChromosomes[self._currentBestSize - 1]].GetFitness() >= self._chromosomes[
                chromosomeIndex].GetFitness()) or self._bestFlags[chromosomeIndex]):
            return

        i = self._currentBestSize
        while i > 0:
            if i < len(self._bestChromosomes):
                if self._chromosomes[self._bestChromosomes[i - 1]].GetFitness() > self._chromosomes[
                    chromosomeIndex].GetFitness():
                    break
                self._bestChromosomes[i] = self._bestChromosomes[i - 1]
            else:
                self._bestFlags[self._bestChromosomes[i - 1]] = False
            i -= 1

        self._bestChromosomes[i] = chromosomeIndex
        self._bestFlags[chromosomeIndex] = True

        if self._currentBestSize < len(self._bestChromosomes):
            self._currentBestSize += 1

    def GetBestChromosome(self):
        return self._chromosomes[self._bestChromosomes[0]]

    def IsInBest(self, chromosomeIndex):
        return self._bestFlags[chromosomeIndex]

    def ClearBest(self):
        for i in xrange(len(self._bestFlags) - 1, -1, -1):
            self._bestFlags[i] = False
        self._currentBestSize = 0

    def parinTable(self, schedule):
        nr = schedule._conf.GetNumberOfRooms()
        it1 = iter(schedule._classes.iteritems())
        size = len(schedule._classes)
        daySize = schedule._config_options.DAY_HOURS * nr
        print 'DaySize: ', daySize
        ci = 0
        for i in xrange(0, size):
            n1 = it1.next()

            cc = n1[0]
            p = n1[1]

            day = p / daySize
            time = p % daySize
            room = time / schedule._config_options.DAY_HOURS + 1
            time = time % schedule._config_options.DAY_HOURS
            dur = cc.GetDuration()

            weekday = self.WeekNames(day)
            p_time = str(time + 8) + ":00 - " + str(time + 8 + dur) + ":00"
            room = schedule._conf._rooms[room].ToString()

            print "День недели:\n\t", weekday
            print "Время:\n\t", p_time
            print cc.ToString()
            print room
            self.printCriteria(schedule._criteria[ci + 0], 0)
            self.printCriteria(schedule._criteria[ci + 1], 1)
            self.printCriteria(schedule._criteria[ci + 2], 2)
            self.printCriteria(schedule._criteria[ci + 3], 3)
            self.printCriteria(schedule._criteria[ci + 4], 4)
            self.printCriteria(schedule._criteria[ci + 5], 5)
            self.printCriteria(schedule._criteria[ci + 6], 6)
            self.printCriteria(schedule._criteria[ci + 7], 7)
            self.printCriteria(schedule._criteria[ci + 8], 8)
            self.printCriteria(schedule._criteria[ci + 9], 9)
            self.printCriteria(schedule._criteria[ci + 10], 10)
            self.printCriteria(schedule._criteria[ci + 11], 11)

            print '\n'
            print '-' * 100
            print '\n'
            ci += schedule._criteria_count

    def printCriteria(self, ok, id):
        if id == 0:
            if ok:
                print cd("criteria 0 true (without concurrent two classes in one room)", "green")
            else:
                print cd("criteria 0 false (without concurrent two classes in one room)", "red")
        elif id == 1:
            if ok:
                print cd("criteria 1 true (does rooms suitable for course (room type))", "green")
            else:
                print cd("criteria 1 false (does rooms suitable for course (room type))", "red")
        elif id == 2:
            if ok:
                print cd("criteria 2 true (Number of Students)", "green")
            else:
                print cd("criteria 2 false (Number of Students)", "red")
        elif id == 3:
            if ok:
                print cd("criteria 3 true (without concurrent classes for Teacher)", "green")
            else:
                print cd("criteria 3 false (without concurrent classes for Teacher)", "red")
        elif id == 4:
            if ok:
                print cd("criteria 4 true (Housing of room and course class)", "green")
            else:
                print cd("criteria 4 false (Housing of room and course class)", "red")
        elif id == 5:
            if ok:
                print cd("criteria 5 true (Sport time)", "green")
            else:
                print cd("criteria 5 false (Sport time)", "red")
        elif id == 6:
            if ok:
                print cd("criteria 6 true (English time and day)", "green")
            else:
                print cd("criteria 6 false (English time and day)", "red")
        elif id == 7:
            if ok:
                print cd("criteria 7 true (Lecture Lab Practice)", "green")
            else:
                print cd("criteria 7 false (Lecture Lab Practice)", "red")
        elif id == 8:
            if ok:
                print cd("criteria 8 true (Professor Housing)", "green")
            else:
                print cd("criteria 8 false (Professor Housing)", "red")
        elif id == 9:
            if ok:
                print cd("criteria 9 true (Additional Options)", "green")
            else:
                print cd("criteria 9 false (Additional Options)", "red")
        elif id == 10:
            if ok:
                print cd("criteria 10 true (Reservations)", "green")
            else:
                print cd("criteria 10 false (Reservations)", "red")
        elif id == 11:
            if ok:
                print cd("criteria 11 true (Student Overlaps)", "green")
            else:
                print cd("criteria 11 false (Student Overlaps)", "red")

    def WeekNames(self, day):
        NAMES = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }
        return NAMES[day]

    def saveGroups(self, courseClass, number):
        conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                   database=Constants.DATABASE)
        conn2 = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                   database=Constants.DATABASE)
        conn.execute_query(
            'SELECT * FROM Edu_SemesterCourseGroups WHERE SemesterCourseID=%d AND ClassTypeID=%d AND Number=%d',
            (courseClass.GetCourse().GetId(), courseClass.GetClassType(), number))
        groupID = 0
        for row in conn:
            groupID = row['ID']

        if groupID == 0:
            print courseClass.GetCourse().GetId(), '    ', courseClass.GetClassType(), '     ', number
            conn.execute_non_query("INSERT INTO Edu_SemesterCourseGroups VALUES(%d, %d, %d, '', Null)",
                                   (courseClass.GetCourse().GetId(), courseClass.GetClassType(), number))

            conn.execute_query(
                'SELECT * FROM Edu_SemesterCourseGroups WHERE SemesterCourseID=%d AND ClassTypeID=%d AND Number=%d',
                (courseClass.GetCourse().GetId(), courseClass.GetClassType(), number))

            for row in conn:
                groupID = row['ID']
                for student in courseClass.GetGroup().GetStudents():
                    conn2.execute_non_query("INSERT INTO Edu_SemesterCourseGroupStudents VALUES(%d, %d)",
                                            (row['ID'], student.GetId()))
                    # time.sleep(0.1)
        conn.close()
        conn2.close()

        return groupID

    def saveSchedule(self, schedule):
        nr = schedule._conf.GetNumberOfRooms()
        it1 = iter(schedule._classes.iteritems())
        size = len(schedule._classes)
        daySize = schedule._config_options.DAY_HOURS * nr
        numbersDict = {}
        ci = 0
        conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                   database=Constants.DATABASE)
        for i in xrange(0, size):
            n1 = it1.next()

            cc = n1[0]  # Courseclass
            p = n1[1]  # position
            if (cc.GetCourse().GetId(), cc.GetClassType()) in numbersDict:
                numbersDict[(cc.GetCourse().GetId(), cc.GetClassType())] += 1
            else:
                numbersDict[(cc.GetCourse().GetId(), cc.GetClassType())] = 1
            groupID = self.saveGroups(cc, numbersDict[(cc.GetCourse().GetId(), cc.GetClassType())])
            day = p / daySize
            time = p % daySize
            room = time / schedule._config_options.DAY_HOURS + 1
            time = time % schedule._config_options.DAY_HOURS  # schedule._times[time % schedule._config_options.DAY_HOURS]
            dur = cc.GetDuration()

            room = schedule._conf._rooms[room]

            course = cc.GetCourse()

            print 'Day: ', day, 'StartTime: ', time + 1, 'EndTime: ', (time + 1) + (
                2 * dur - 1), 'Room: ', room.GetDbId(),
            conn.execute_non_query(
                "INSERT INTO Edu_SemesterCourseSections (SemesterCourseID, ClassTypeID, DayID, StartID, EndID, RoomID, InstructorID, CourseGroupID, LastUpdatedBy, LastUpdatedOn)VALUES(%d, %d, %d, %d, %d, %d, %d, %d, 'E9E50C0F-1E46-4816-99B6-75722F06008F', %s)",
                (course.GetId(), cc.GetClassType(), day + 1, time + 1, (time + 1) + (2 * dur - 1), room.GetDbId(),
                 cc.GetProfessor().GetId(), groupID, datetime.datetime.now()))

            # self.conn.execute_non_query("INSERT INTO Edu_SemesterCourseSections VALUES(course.GetId(), cc.GetClassType(), day, time, time+(2*dur-1), room.GetId(), cc.GetProfessor().GetId(), 1, 1)")


# helper = DatabaseHelper(1, 1, '2017', 1)
# times = helper.getTimes()
# days = helper.getDays()
#
# [c, ad_options] = helper.readSettings()
# # c.set_voenka_day(3)
# # c.set_bekturova_day(4)
# print c.toString()
#
# rooms = helper.getRooms()
# teachers = helper.getTeachers()
# students = helper.getStudents()
# courses = helper.getCourses()
# courseClasses = helper.getCourseClasses()
# # print 'Length1: ', len(courseClasses)
#
# courseClasses = helper.createCourseClasses()
# # print 'Length2: ', len(courseClasses)
#
# roomReservations = helper.getRoomReservations()
#
# conf = Configuration(rooms, teachers, courses, courseClasses, roomReservations, ad_options, times, days)
#
# s = Schedule(10, 3, 70, 10, c, conf)
# a = Algorithm(100, 10, 5, s)
# a.Start()

# for cc in conf._professors[1]._courseClasses:
# print a._chromosomes[0]._classes[cc], cc
