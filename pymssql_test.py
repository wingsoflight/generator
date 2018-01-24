from DatabaseHelper import DatabaseHelper

# helper = DatabaseHelper()
# helper.getRooms()
# helper.getTeachers()
# helper.getStudents()
# helper.getCourses()
# helper.getCourseClasses()
# helper.createCourseClasses()
# helper.readSettings()


import _mssql
from Constants import Constants




conn = _mssql.connect(server=Constants.SERVER_IP, user=Constants.USER, password=Constants.PASSWORD,
                                  database=Constants.DATABASE)



conn.execute_row(Constants.INSTRUCTOR_CONFLICT_QUERY, (1, 1, 1, 1, 1))


