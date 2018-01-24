# -*- coding: utf-8 -*-

import _mssql
from Room import Room
from Professor import Professor
from Course import Course
from CourseClass import CourseClass
from StudentGroup import StudentGroup
from Student import Student
from Reservation import Reservation
from Time import Time
from Day import Day
from AdditionalOption import AdditionalOption
from Constants import Constants
from ConfigOptions import ConfigOptions
import json
from datetime import datetime


class DatabaseHelper(object):
    def __init__(self, semesterId, yearOfAdmission, isBachelor, scheduleInfoId):
        super(DatabaseHelper, self).__init__()
        self._scheduleInfoId = scheduleInfoId
        self._isBachelor = isBachelor
        self._semesterId = semesterId
        self._yearOfAdmission = yearOfAdmission
        self._courses = {}
        self._rooms = {}
        self._professors = {}
        self._courseClasses = []
        self._courseClassesMain = []
        self._groupedCourseClasses = {}
        self._reservations = {}
        self._studentGroups = []
        self._times = {}
        self._days = {}
        self._students = {}
        self.conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                   database=Constants.DATABASE)
        self.conn2 = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                    database=Constants.DATABASE)
        self.conn3 = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                    database=Constants.DATABASE)

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def getRooms(self):
        self.conn.execute_query('SELECT * FROM Edu_Rooms WHERE Active=1')
        rooms = {}
        i = 1
        for row in self.conn:
            self.conn2.execute_query('SELECT * FROM Edu_CourseRooms')
            is_special_room = False
            special_course = 'все'
            for special_row in self.conn2:
                if special_row['RoomID'] == row['ID']:
                    is_special_room = True
                    special_course = special_row['CourseID']
                    # print 'True'
                    break
            room = Room(i, row['ID'], row['BuildingID'], row['Title'], row['Capacity'], row['TypeID'], is_special_room,
                        special_course)
            rooms[i] = room
            i += 1

        # print 'Rooms count: ', len(rooms)
        self._rooms = rooms
        return rooms

    def getTeachers(self):
        self.conn.execute_query('SELECT * FROM EmployeesAll')
        professors = {}

        for row in self.conn:
            professor = Professor(row['Id'], row['Title'])
            professors[row['Id']] = professor

        # print 'Professors count: ', len(professors)
        self._professors = professors
        return professors

    def getCourses(self):
        currentMonth = datetime.now().month
        currentYear = datetime.now().year

        if currentMonth < 7:
            currentYear -= 1
        generateForJunior = False
        if self.RepresentsInt(self._yearOfAdmission) and int(self._yearOfAdmission) == currentYear:
        # if len(self._yearOfAdmission) == 1 and self._yearOfAdmission[0] == currentYear:
            generateForJunior = True

        self.conn.execute_query(Constants.DELETE_COURSE_GROUPS, (
            currentYear, self._semesterId, self._yearOfAdmission, self._isBachelor, self._isBachelor, self._isBachelor,
            generateForJunior))

        self.conn.execute_query(Constants.SELECT_COURSES_QUERY, (
            currentYear, self._semesterId, self._yearOfAdmission, self._isBachelor, self._isBachelor, self._isBachelor,
            generateForJunior))
        courses = {}

        for row in self.conn:
            self.conn2.execute_query('SELECT * FROM Edu_CourseRooms WHERE CourseID=%d', row['ID'])
            is_special_room = False
            building_id = 0

            for special_row in self.conn2:
                is_special_room = True
                self.conn3.execute_query('SELECT * FROM Edu_Rooms WHERE ID=%d', special_row['RoomID'])
                for building_row in self.conn3:
                    building_id = building_row['BuildingID']
                    # print 'BuildingID: ', building_id
                    # print 'True'

            course = Course(row['ID'], row['Code'], row['Title'], is_special_room, building_id, row['OrgUnitID'],
                            row['Lectures'], row['Labs'], row['Practices'])
            courses[row['ID']] = course

        print 'Courses count: ', len(courses)
        self._courses = courses
        # print 'Course Lectures: ', self._courses[33].GetLectures()
        # print 'Course Labs: ', self._courses[33].GetLabs()
        # print 'Course Practices: ', self._courses[33].GetPractices()

        return courses

    def getCourseStudents(self, course_id):
        self.conn.execute_query('SELECT * FROM Edu_StudentCourses WHERE SemesterCourseID=%d', course_id)
        students = []
        for row in self.conn:
            students.append(self._students[row['StudentID']])

        return students

    def getStudents(self):
        self.conn.execute_query('SELECT * FROM Edu_Students')
        students = {}
        for row in self.conn:
            student = Student(row['StudentID'], row['SpecialityID'], row['Year'])
            students[row['StudentID']] = student

        self._students = students
        print 'Students count: ', len(students)
        return students

    # TODO finish method

    def createCourseClasses(self):
        for key, course in self._courses.iteritems():
            if course.GetId() in self._groupedCourseClasses:
                # print course.GetId()
                students = self.getCourseStudents(course.GetId())
                courseClasses = self._groupedCourseClasses[course.GetId()]
                # print 'Students: ', len(students)
                # print 'CourseClasses: ', len(courseClasses)
                # counter += len(courseClasses)
                # if len(students) == 0:
                # 		for cc in courseClasses:
                # 				self._courseClassesMain.append(cc)


                # lectures = course.GetLectures()
                # labs = course.GetLabs()
                # practices = course.GetPractices()
                #
                # for cc in
                # for i in len(lectures):
                #     cc.SetGroup(studentGroup)


                for student in students:
                    lectures = course.GetLectures()
                    labs = course.GetLabs()
                    practices = course.GetPractices()
                    lectureInstructor = None
                    practiceInstructor = None
                    labInstructor = None
                    for cc in courseClasses:
                        studentGroup = cc.GetGroup()
                        # print cc.GetName(),'   ', len(studentGroup.GetStudents()), '   ', studentGroup.GetNumberOfStudents()
                        # print 'lectures: ', lectures, '   ','labs: ', labs, '   ', 'practices: ', practices
                        if len(studentGroup.GetStudents()) < studentGroup.GetNumberOfStudents():
                            if (cc.GetName() == Constants.LECTURE_ID and lectures > 0) and (
                                            lectureInstructor == None or lectureInstructor == cc.GetProfessor().GetId()):
                                studentGroup.GetStudents().append(student)
                                lectures -= 1
                                lectureInstructor = cc.GetProfessor().GetId()
                            elif (cc.GetName() == Constants.LAB_ID and labs > 0) and (
                                            labInstructor == None or labInstructor == cc.GetProfessor().GetId()):
                                studentGroup.GetStudents().append(student)
                                labs -= 1
                                labInstructor = cc.GetProfessor().GetId()
                            elif (cc.GetName() == Constants.PRACTICE_ID and practices > 0) and (
                                            practiceInstructor == None or practiceInstructor == cc.GetProfessor().GetId()):
                                studentGroup.GetStudents().append(student)
                                practices -= 1
                                practiceInstructor = cc.GetProfessor().GetId()
                        cc.SetGroup(studentGroup)
                        # print 'Student Group: ', len(studentGroup.GetStudents())
                for cc in courseClasses:
                    self._courseClassesMain.append(cc)

        self._courseClasses = self._courseClassesMain
        print 'CourseClasses count2: ', len(self._courseClasses)

        return self._courseClasses

    def getCourseClasses(self):
        self.conn.execute_query('SELECT * FROM Edu_CourseWorkLoad_CourseGroups ORDER BY InstructorID, ClassTypeID')
        courseClasses = []

        for row in self.conn:
            if row['SemesterCourseID'] in self._courses:
                if row['InstructorID'] != None:
                    studentGroup = StudentGroup(row['StudentCount'], 0, [])  # TODO replace or delete 0
                    room_type = 0
                    course = self._courses[row['SemesterCourseID']]
                    # if course.IsSpecialRoom():
                    # 	room_type = 2
                    count = 1
                    if row['ClassTypeID'] == Constants.LECTURE_ID:
                        room_type = 1
                        count = course.GetLectures()
                    elif row['ClassTypeID'] == Constants.PRACTICE_ID:
                        room_type = 2
                        count = course.GetPractices()
                    else:
                        room_type = 3
                        count = course.GetLabs()

                    duration = 1

                    if row['ClassTypeID'] == Constants.LAB_ID:
                        duration = 2

                    # print 'Duration: ', duration
                    self._studentGroups.append(studentGroup)
                    # print row['InstructorID']
                    for i in range(0, count):
                        courseClass = CourseClass(row['ID'], row['ClassTypeID'], row['ClassTypeID'],
                                                  self._professors[row['InstructorID']], course, studentGroup, room_type,
                                                  duration, i)
                        courseClasses.append(courseClass)
                        if not course.GetId() in self._groupedCourseClasses:
                            self._groupedCourseClasses[course.GetId()] = []
                        self._groupedCourseClasses[course.GetId()].append(courseClass)
        print 'CourseClasses count: ', len(courseClasses)
        print 'Grouped Classes: ', len(self._groupedCourseClasses)
        self._courseClasses = courseClasses
        return courseClasses

    def getRoomReservations(self):
        self.conn.execute_query('SELECT * FROM Edu_RoomReservations')
        reservations = {}
        for row in self.conn:
            reservation = Reservation(row['RoomID'], row['DayID'], row['StartID'], row['EndID'])
            reservations[row['RoomID']] = []
            reservations[row['RoomID']].append(reservation)

        self._reservations = reservations
        return reservations

    def getTimes(self):
        self.conn.execute_query('SELECT * FROM Edu_Times WHERE EndOfInterval = 0')
        times = {}
        for row in self.conn:
            time = Time(row['ID'], row['Title'], row['EndOfInterval'])
            times[row['ID']] = time

        self._times = times
        print 'Times: ', len(self._times)
        return times

    def getDays(self):
        self.conn.execute_query('SELECT * FROM Edu_Days')
        days = {}
        for row in self.conn:
            day = Day(row['ID'], row['Title'])
            days[row['ID']] = day

        self._days = days
        print 'Days: ', len(self._days)
        return days

    def readSettings(self):
        self.conn.execute_query('SELECT * FROM Edu_Semesters_ScheduleInfo WHERE ID = %d', self._scheduleInfoId)
        ad_options = []
        for row in self.conn:
            json_string = row['Settings']
            obj = json.loads(json_string)
            for option in obj['additionalOptions']:
                ad_option = AdditionalOption(option['yearOfAdmission'], option['specialityId'], option['courseId'],
                                             option['buildingId'], option['dayOfWeekId'])
                ad_options.append(ad_option)
        co = ConfigOptions(self._yearOfAdmission, len(self._times), len(self._days), self._semesterId)
        return [co, ad_options]

    def saveGroups(self, courceClass):
        for student in courceClass.GetGroup():
            if courceClass.GetNumber() == 0:
                self.conn.execute_non_query("INSERT INTO Edu_SemesterCourseGroupStudents VALUES(%d, %d)",
                                            (courceClass.GetId(), student.GetId()))

    # def generateWorkload(self):
    #     self.conn.execute_query('SELECT * FROM Edu_SemesterCourseSections')
    #     for row in self.conn:
    #         self.conn2.execute_non_query("INSERT INTO Edu_CourseWorkLoad_CourseGroups VALUES(%d, %d, 1, %d, 1)",
    #                                      (row['SemesterCourseID'], row['ClassTypeID'], row['InstructorID']))

    def saveSchedule(self, schedule):
        nr = schedule._conf.GetNumberOfRooms()
        it1 = iter(schedule._classes.iteritems())
        size = len(schedule._classes)
        daySize = schedule._config_options.DAY_HOURS * nr
        ci = 0
        # for i in xrange(0, size):
        #   n1 = it1.next()

        #   cc = n1[0]  # Courseclass
        #   p = n1[1]  # position
        #   saveGroups(cc)
        #   day = p / daySize
        #   time = p % daySize
        #   room = time / schedule._config_options.DAY_HOURS + 1
        #   time = time % schedule._config_options.DAY_HOURS
        #   dur = cc.GetDuration()

        #   room = schedule._conf._rooms[room]

        #   course = cc.getCourse()

        #   self.conn.execute_non_query("INSERT INTO Edu_SemesterCourseSections VALUES(1, %d, %d, %d, %d, %d, %d, %d, %d, %d, 1, 1)", (course.GetId(), cc.getName(), day, time, time+dur, room.GetId(), time, time+dur, cc.GetProfessor().GetId()))








        # helper = DatabaseHelper()
        # helper.generateWorkload()
