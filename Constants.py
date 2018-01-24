# -*- coding: utf-8 -*-

class Constants(object):
    LECTURE_ID = 3
    LAB_ID = 1
    PRACTICE_ID = 2

    LECTURE_ROOM = 1
    PRACTICE_ROOM = 2
    LAB_ROOM = 3

    SERVER_IP = '192.168.150.24'
    USER = 'developer'
    PASSWORD = 'KMG123321'
    DATABASE = 'KazNITU_Test'
    QUEUE_NAME = 'KaznituSchedule'
    QUEUE_USER = 'user'
    QUEUE_PASSWORD = 'WdfY3BCh'

    ROOM_CONFLICT_QUERY = 'DECLARE @RoomIDs dbo.IdList;' \
                                + 'INSERT INTO @RoomIDs(Id) VALUES(%d);' \
                                + 'DECLARE @TimeRanges dbo.TimeRange;' \
                                + 'INSERT INTO @TimeRanges(DayOfWeekId, StartTimeId, EndTimeId) VALUES (%d,%d,%d);' \
                                + 'DECLARE @semesterId INT = %d;' \
                                + 'EXEC Edu_Schedule_CheckRoomsForConflicts @RoomIDs, @TimeRanges, @semesterId;'


    INSTRUCTOR_CONFLICT_QUERY = 'DECLARE @instructorIds dbo.IdList;' \
                          + 'INSERT INTO @instructorIds(Id) VALUES(%d);' \
                          + 'DECLARE @TimeRanges dbo.TimeRange;' \
                          + 'INSERT INTO @TimeRanges(DayOfWeekId, StartTimeId, EndTimeId) VALUES (%d,%d,%d);' \
                          + 'DECLARE @semesterId INT = %d;' \
                          + 'EXEC Edu_Schedule_CheckInstructorsForConflicts @instructorIds, @TimeRanges, @semesterId;'

    SELECT_COURSES_QUERY = 'select distinct sc.ID, sc.Code, sc.Title, sc.OrgUnitID, sc.Lectures, sc.Labs, sc.Practices from Edu_Students stud join Edu_Users us on us.ID = stud.StudentID join Edu_Rups rup on rup.ID = stud.RupID join Edu_Specialities spec on spec.ID = stud.SpecialityID join Edu_StudentCourses studCours on studCours.StudentID = stud.StudentID join Edu_SemesterCourses sc on sc.Id = studCours.SemesterCourseID outer apply ( select count(*) Cnt from Edu_StudentCourses tsc join Edu_Students tstud on tstud.StudentID = tsc.StudentID join Edu_Specialities tspec on tspec.ID = tstud.SpecialityID where tsc.SemesterCourseID = sc.ID and tspec.LevelID = 1 ) bachelorStuds outer apply ( select count(*) Cnt from Edu_StudentCourses tsc join Edu_Students tstud on tstud.StudentID = tsc.StudentID join Edu_Rups trup on trup.ID = tstud.RupID where tsc.SemesterCourseID = sc.ID and trup.Year = %s ) juniorStuds where sc.SemesterID = %d and charindex(cast(rup.Year as nvarchar(200)), %s) > 0 and ((%d = 0 and spec.LevelID <> 1) or (%d = 1 and spec.LevelID = 1)) and (%d = 1 or bachelorStuds.Cnt = 0) and (%d = 1 or juniorStuds.Cnt = 0);'

    DELETE_COURSE_GROUPS = 'delete gr from Edu_Students stud join Edu_Users us on us.ID = stud.StudentID join Edu_Rups rup on rup.ID = stud.RupID join Edu_Specialities spec on spec.ID = stud.SpecialityID join Edu_StudentCourses studCours on studCours.StudentID = stud.StudentID join Edu_SemesterCourses sc on sc.Id = studCours.SemesterCourseID outer apply ( select count(*) Cnt from Edu_StudentCourses tsc join Edu_Students tstud on tstud.StudentID = tsc.StudentID join Edu_Specialities tspec on tspec.ID = tstud.SpecialityID where tsc.SemesterCourseID = sc.ID and tspec.LevelID = 1 ) bachelorStuds outer apply ( select count(*) Cnt from Edu_StudentCourses tsc join Edu_Students tstud on tstud.StudentID = tsc.StudentID join Edu_Rups trup on trup.ID = tstud.RupID where tsc.SemesterCourseID = sc.ID and trup.Year = %d ) juniorStuds join Edu_SemesterCourseGroups gr on gr.SemesterCourseID = sc.ID where sc.SemesterID = %d and charindex(cast(rup.Year as nvarchar(200)), %s) > 0 and ((%d = 0 and spec.LevelID <> 1) or (%d = 1 and spec.LevelID = 1)) and (%d = 1 or bachelorStuds.Cnt = 0) and (%d = 1 or juniorStuds.Cnt = 0);'
