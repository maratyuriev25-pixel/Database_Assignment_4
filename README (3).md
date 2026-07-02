
Зв'язки 

1:many (одне-до-багатьох):**
- COURSES → SCHEDULE (1 курс має багато занять)
- COURSES → STUDENTS_COURSE_GROUPS (1 курс має багато груп)
- INSTRUCTORS → SCHEDULE (1 викладач має багато занять)
- ROOMS → SCHEDULE (1 аудиторія використовується багато разів)

many:many (багато-до-багатьох):**
- INSTRUCTORS ↔ COURSES (через INSTRUCTORS_COURSES)
  Один викладач вчить багато курсів, один курс викладають багато викладачів
- STUDENTS ↔ STUDENT_GROUPS (через STUDENTS_COURSE_GROUP_STUDENTS)
  Один студент у багато групах, одна група має багато студентів



Обмеження

PRIMARY KEY: Кожна таблиця має унікальний ідентифікатор

FOREIGN KEY: SCHEDULE.COURSE_ID → COURSES.ID
- SCHEDULE.INSTRUCTOR_ID → INSTRUCTORS.ID
- SCHEDULE.ROOM_ID → ROOMS.ID

UNIQUE: Унікальні значення
- STUDENTS.EMAIL
- INSTRUCTORS.EMAIL
- COURSES.COURSE_DISPLAY_SHORT_NAME
- ROOMS(BUILDING, FLOOR, NUMBER) - комбінація унікальна

CHECK: Перевірка значень
- STUDENTS.COURSE (1-6)
- ROOMS.SEATS_NUMBER (>0)
- LESSONS_SCHEDULE.START_TIME < END_TIME
- SCHEDULE.WEEK_DAY IN ('MONDAY', ..., 'SUNDAY')

NOT NULL: Обов'язкові значення
- STUDENTS.FIRST_NAME, LAST_NAME, EMAIL
- INSTRUCTORS.FIRST_NAME, LAST_NAME, EMAIL



Індекси

Single-Column Indexes
idx_students_email, idx_students_active, idx_courses_short_name, idx_instructors_email

Foreign Key Indexes
idx_schedule_course, idx_schedule_instructor, idx_schedule_room, idx_students_group_students_student

Composite Indexes
idx_schedule_course_day_time - пошук по курсу, дню, часу

Performance Results
- Без індексу: 300-500ms (500K рядків сканується)
- З індексом: 2-5ms


Тригери


Trigger 1: log_students_changes()
Автоматично логує INSERT, UPDATE, DELETE на таблиці STUDENTS.

Записує в AUDIT_LOG:
- TABLE_NAME, OPERATION, RECORD_ID
- OLD_VALUES (для UPDATE/DELETE)
- NEW_VALUES (для INSERT/UPDATE)
- CHANGED_BY, CHANGED_AT

Trigger 2: check_instructor_course()
BEFORE INSERT/UPDATE на SCHEDULE

Перевіряє чи цей викладач вчить цей курс

Trigger 3: check_room_capacity()
BEFORE INSERT/UPDATE на SCHEDULE

Перевіряє чи кімната вміщує групу



Stored procedures

Procedure 1: get_student_schedule(p_student_id)
Отримує розклад студента на тиждень

Procedure 2: enroll_student_in_course(p_student_id, p_group_id)
Реєструє студента в групу з валідацією.


Ролі/користвуачі

1. admin_user
Привілеї: GRANT ALL PRIVILEGES ON ALL TABLES
Доступ: Повний

2. faculty_user
Привілеї: SELECT курсів, видів розкладу, UPDATE свого профілю
Доступ: Для викладачів

3. student_user
Привілеї: SELECT курсів, свого розкладу
Доступ: Для студентів (read-only)

4. audit_user
Привілеї: SELECT на всі таблиці, SELECT AUDIT_LOG
Доступ: Для аудиторів (read-only)


 	
View

1. STUDENT_SCHEDULE - Розклад студента на тиждень
2. INSTRUCTOR_SCHEDULE - Розклад викладача з кількістю студентів
3. COURSE_STATISTICS - Статистика по курсам
4. ROOM_UTILIZATION - Використання аудиторій
5. INACTIVE_USERS - Неактивні студенти й викладачі

