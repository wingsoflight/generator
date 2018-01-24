#!/usr/bin/env python
import pika
import json
from Schedule import Schedule
from ConfigOptions import ConfigOptions
from Configuration import Configuration
from DatabaseHelper import DatabaseHelper
from Algorithm import Algorithm
import threading
import _mssql
from Constants import Constants

# credentials = pika.PlainCredentials(Constants.QUEUE_USER, Constants.QUEUE_PASSWORD)
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='192.168.12.104', credentials=credentials, virtual_host='/'))
# channel = connection.channel()

threads = {}


def start_algorithm(scheduleInfoId):
    conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                               database=Constants.DATABASE)
    conn.execute_query('SELECT * FROM Edu_Semesters_ScheduleInfo WHERE ID = %d', scheduleInfoId)

    semesterId = 0
    isBachelor = True
    yearOfAdmission = ''
    for row in conn:
        j = json.loads(row['Settings'])
        semesterId = j['semesterId']
        isBachelor = j['isBachelor']
        yearOfAdmission = j['yearsOfAdmission']

    helper = DatabaseHelper(semesterId, yearOfAdmission, isBachelor, scheduleInfoId)
    times = helper.getTimes()
    days = helper.getDays()

    [c, ad_options] = helper.readSettings()
    # c.set_voenka_day(3)
    # c.set_bekturova_day(4)
    print c.toString()

    rooms = helper.getRooms()
    teachers = helper.getTeachers()
    students = helper.getStudents()
    courses = helper.getCourses()
    courseClasses = helper.getCourseClasses()
    # print 'Length1: ', len(courseClasses)

    courseClasses = helper.createCourseClasses()
    # print 'Length2: ', len(courseClasses)

    if len(courseClasses) > 0:
        roomReservations = helper.getRoomReservations()

        conf = Configuration(rooms, teachers, courses, courseClasses, roomReservations, ad_options, times, days)

        conn.execute_non_query(
            'UPDATE Edu_Semesters_ScheduleInfo SET StatusID = 2 WHERE ID = %d',
            scheduleInfoId)
        s = Schedule(10, 3, 70, 10, c, conf)
        a = Algorithm(100, 10, 5, s, scheduleInfoId)
        a.Start()
    else: conn.execute_non_query(
            'UPDATE Edu_Semesters_ScheduleInfo SET StatusID = 3 WHERE ID = %d',
        scheduleInfoId)


# channel.queue_declare(queue='KaznituExamSchedule')
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                          database=Constants.DATABASE)
    try:
        j = json.loads(body)

        if j['type'] == 1:
            t = threading.Thread(target=start_algorithm, args=(j['id'], ))
            t.start()
            threads[j['id']] = t
        else:
            t = threads[j['id']]
            t.isStopped = True
            t.join()
            # algos[j['id']].Stop()
            # del algos[j['id']]
    except:
        conn.execute_non_query(
            'UPDATE Edu_Semesters_ScheduleInfo SET StatusID = 3 WHERE ID = %d', j['id'])
        print 'Error Occured'

data = {}
data['id'] = 2004
data['type'] = 1
callback(None, None, None, json.dumps(data))