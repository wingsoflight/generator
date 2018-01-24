declare @yearsOfAdmission nvarchar(200) = '2017|2016|2015|2014';
declare @isBachelor bit = 0;
declare @semesterId int = 1;

declare @juniorYear int = iif(
 datepart(month, getdate()) < 7,
 datepart(year, getdate()) - 1,
 datepart(year, getdate())
);
declare @generateForJunior bit = iif(isnumeric(@yearsOfAdmission) = 1 and cast(@yearsOfAdmission as int) = @juniorYear, 1, 0);

select distinct
 sc.ID,
 sc.Code,
 sc.Title,
 sc.OrgUnitID,
 sc.Lectures,
 sc.Labs,
 sc.Practices
from
Edu_Students stud
join Edu_Users us on us.ID = stud.StudentID
join Edu_Rups rup on rup.ID = stud.RupID
join Edu_Specialities spec on spec.ID = stud.SpecialityID

join Edu_StudentCourses studCours on studCours.StudentID = stud.StudentID
join Edu_SemesterCourses sc on sc.Id = studCours.SemesterCourseID

outer apply (
 select
 count(*) Cnt
 from Edu_StudentCourses tsc
 join Edu_Students tstud on tstud.StudentID = tsc.StudentID
 join Edu_Specialities tspec on tspec.ID = tstud.SpecialityID
 where tsc.SemesterCourseID = sc.ID and tspec.LevelID = 1
) bachelorStuds

outer apply (
 select
 count(*) Cnt
 from Edu_StudentCourses tsc
 join Edu_Students tstud on tstud.StudentID = tsc.StudentID
 join Edu_Rups trup on trup.ID = tstud.RupID
 where tsc.SemesterCourseID = sc.ID and trup.Year = @juniorYear
) juniorStuds

where
sc.SemesterID = @semesterId and
charindex(cast(rup.Year as nvarchar(200)), @yearsOfAdmission) > 0 and
((@isBachelor = 0 and spec.LevelID <> 1) or (@isBachelor = 1 and spec.LevelID = 1)) and
(@isBachelor = 1 or bachelorStuds.Cnt = 0) and
(@generateForJunior = 1 or juniorStuds.Cnt = 0);


delete gr
from
Edu_Students stud
join Edu_Users us on us.ID = stud.StudentID
join Edu_Rups rup on rup.ID = stud.RupID
join Edu_Specialities spec on spec.ID = stud.SpecialityID

join Edu_StudentCourses studCours on studCours.StudentID = stud.StudentID
join Edu_SemesterCourses sc on sc.Id = studCours.SemesterCourseID

outer apply (
 select
 count(*) Cnt
 from Edu_StudentCourses tsc
 join Edu_Students tstud on tstud.StudentID = tsc.StudentID
 join Edu_Specialities tspec on tspec.ID = tstud.SpecialityID
 where tsc.SemesterCourseID = sc.ID and tspec.LevelID = 1
) bachelorStuds

outer apply (
 select
 count(*) Cnt
 from Edu_StudentCourses tsc
 join Edu_Students tstud on tstud.StudentID = tsc.StudentID
 join Edu_Rups trup on trup.ID = tstud.RupID
 where tsc.SemesterCourseID = sc.ID and trup.Year = @juniorYear
) juniorStuds

join Edu_SemesterCourseGroups gr on gr.SemesterCourseID = sc.ID

where
sc.SemesterID = @semesterId and
charindex(cast(rup.Year as nvarchar(200)), @yearsOfAdmission) > 0 and
((@isBachelor = 0 and spec.LevelID <> 1) or (@isBachelor = 1 and spec.LevelID = 1)) and
(@isBachelor = 1 or bachelorStuds.Cnt = 0) and
(@generateForJunior = 1 or juniorStuds.Cnt = 0);


