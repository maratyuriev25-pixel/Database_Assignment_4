import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from faker import Faker
import uuid
import random
from datetime import time
import sys

load_dotenv("credentials.env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Debug: Print what was loaded
if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    print("⚠ Warning: Missing environment variables!")
    print(f"  DB_HOST: {DB_HOST}")
    print(f"  DB_PORT: {DB_PORT}")
    print(f"  DB_NAME: {DB_NAME}")
    print(f"  DB_USER: {DB_USER}")
    print(f"  DB_PASSWORD: {'***' if DB_PASSWORD else 'NOT SET'}")

NUM_INSTRUCTORS = 50
NUM_COURSES = 30
NUM_STUDENTS = 5000
NUM_ROOMS = 40
NUM_SCHEDULES = 500000

fake = Faker()


class DatabaseSeeder:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            print(f"Connecting to {DB_HOST}:{DB_PORT}/{DB_NAME}...")
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=int(DB_PORT),
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            self.cursor = self.conn.cursor()
            print("✓ Connected successfully")
        except psycopg2.Error as e:
            print(f"✗ Connection failed: {e}")
            sys.exit(1)

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"✗ Query failed: {e}")
            raise

    def executemany(self, query, data):
        try:
            self.cursor.executemany(query, data)
            self.conn.commit()
            print(f"✓ Inserted {len(data)} rows")
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"✗ Batch insert failed: {e}")
            raise

    def _truncate_phone(self, phone):
        if phone is None:
            return None
        phone_str = str(phone).strip()
        if len(phone_str) > 20:
            phone_str = phone_str[:20]
        return phone_str

    def clear_tables(self):
        tables_to_clear = [
            'SCHEDULE',
            'STUDENTS_COURSE_GROUP_STUDENTS',
            'STUDENTS_COURSE_GROUPS',
            'INSTRUCTORS_COURSES',
            'STUDENTS',
            'INSTRUCTORS',
            'COURSES',
            'ROOMS',
            'LESSONS_SCHEDULE',
            'AUDIT_LOG'
        ]

        print("Clearing tables...")
        for table in tables_to_clear:
            try:
                self.execute_query(f"TRUNCATE TABLE {table} CASCADE")
                print(f"  {table}")
            except psycopg2.Error as e:
                print(f"  {table} (skipped: {e})")

    def seed_lessons_schedule(self):
        lesson_times = [
            (1, time(8, 0), time(9, 30)),
            (2, time(9, 45), time(11, 15)),
            (3, time(11, 30), time(13, 0)),
            (4, time(14, 0), time(15, 30)),
            (5, time(15, 45), time(17, 15)),
            (6, time(17, 30), time(19, 0)),
        ]

        query = "INSERT INTO LESSONS_SCHEDULE (ID, START_TIME, END_TIME) VALUES (%s, %s, %s)"

        for lesson_id, start_time, end_time in lesson_times:
            try:
                self.execute_query(query, (lesson_id, start_time, end_time))
            except psycopg2.Error:
                pass

    def seed_rooms(self):
        buildings = ['Building A', 'Building B', 'Building C', 'Building D']
        rooms_data = []

        for building in buildings:
            for floor in range(1, 4):
                for room_num in range(1, 11):
                    room_id = str(uuid.uuid4())
                    seats = random.choice([30, 40, 50, 60])
                    display_name = f"{building} Floor {floor} Room {room_num}"

                    rooms_data.append((
                        room_id,
                        building,
                        floor,
                        room_num,
                        display_name,
                        seats
                    ))

        query = """
            INSERT INTO ROOMS (ID, BUILDING, FLOOR, NUMBER, DISPLAY_NAME, SEATS_NUMBER)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        self.executemany(query, rooms_data)
        return [room[0] for room in rooms_data]

    def seed_courses(self):
        course_data = [
            ('CS101', 'Introduction to Programming', 'Learn programming fundamentals', 30, 15),
            ('CS102', 'Data Structures', 'Master data structures and algorithms', 25, 20),
            ('CS103', 'Database Design', 'Design and implement databases', 20, 25),
            ('CS104', 'Web Development', 'Build modern web applications', 20, 30),
            ('CS105', 'Machine Learning', 'Introduction to ML and AI', 15, 10),
            ('MATH101', 'Calculus I', 'Differential calculus', 40, 20),
            ('MATH102', 'Linear Algebra', 'Vectors and matrices', 35, 15),
            ('PHYS101', 'Physics I', 'Mechanics and motion', 30, 20),
            ('ENG101', 'English Literature', 'Classic and modern literature', 25, 10),
            ('ENG102', 'Writing Skills', 'Academic and professional writing', 20, 15),
            ('HIST101', 'World History', 'Ancient to modern history', 35, 5),
            ('CHEM101', 'Chemistry I', 'General chemistry', 25, 25),
            ('BIO101', 'Biology I', 'Cell biology and genetics', 30, 20),
            ('ECON101', 'Microeconomics', 'Economic principles', 40, 10),
            ('PSYCH101', 'Introduction to Psychology', 'Human behavior and mind', 45, 5),
        ]

        courses = {}
        query = """
            INSERT INTO COURSES (ID, COURSE_DISPLAY_SHORT_NAME, COURSE_DISPLAY_FULL_NAME,
                                COURSE_DESCRIPTION, LECTURES_NUM, PRACTICES_NUM)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        for short_name, full_name, desc, lectures, practices in course_data:
            course_id = str(uuid.uuid4())
            self.execute_query(query, (course_id, short_name, full_name, desc, lectures, practices))
            courses[short_name] = course_id

        return courses

    def seed_instructors(self):
        instructors_data = []
        instructors = {}

        for i in range(NUM_INSTRUCTORS):
            instructor_id = str(uuid.uuid4())
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{i}@university.edu"
            phone = self._truncate_phone(fake.phone_number())

            instructors_data.append((
                instructor_id,
                first_name,
                last_name,
                email,
                phone,
                True
            ))

            instructors[instructor_id] = (first_name, last_name, email)

        query = """
            INSERT INTO INSTRUCTORS (ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, ACTIVE)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        self.executemany(query, instructors_data)
        return list(instructors.keys())

    def seed_instructor_courses(self, instructor_ids, courses):
        assignments = []
        course_ids = list(courses.values())

        for instructor_id in instructor_ids:
            num_courses = random.randint(2, 4)
            assigned_courses = random.sample(course_ids, min(num_courses, len(course_ids)))

            for course_id in assigned_courses:
                assignments.append((instructor_id, course_id))

        query = """
            INSERT INTO INSTRUCTORS_COURSES (INSTRUCTOR_ID, COURSE_ID)
            VALUES (%s, %s)
        """

        self.executemany(query, assignments)

    def seed_students(self):
        students_data = []
        student_ids = []
        degrees = ['Bachelor', 'Master', 'PhD']
        specialities = ['Computer Science', 'Engineering', 'Mathematics', 'Physics', 'Chemistry']

        for i in range(NUM_STUDENTS):
            student_id = str(uuid.uuid4())
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}{i}@student.university.edu"
            phone = self._truncate_phone(fake.phone_number())
            course = random.randint(1, 4)
            degree = random.choice(degrees)
            speciality = random.choice(specialities)

            students_data.append((
                student_id,
                first_name,
                last_name,
                email,
                phone,
                course,
                degree,
                speciality,
                True
            ))

            student_ids.append(student_id)

        query = """
            INSERT INTO STUDENTS (ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, COURSE,
                                 EDUCATIONAL_DEGREE, SPECIALITY, ACTIVE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        batch_size = 1000
        for i in range(0, len(students_data), batch_size):
            batch = students_data[i:i+batch_size]
            self.executemany(query, batch)

        return student_ids

    def seed_student_course_groups(self, courses):
        groups_data = []
        groups = {}
        course_ids = list(courses.values())

        for course_id in course_ids:
            num_groups = random.randint(3, 5)
            for group_num in range(1, num_groups + 1):
                group_id = str(uuid.uuid4())
                groups_data.append((group_id, course_id, group_num))
                groups[group_id] = course_id

        query = """
            INSERT INTO STUDENTS_COURSE_GROUPS (ID, COURSE_ID, GROUP_NUMBER)
            VALUES (%s, %s, %s)
        """

        self.executemany(query, groups_data)
        return list(groups.keys())

    def seed_student_group_membership(self, student_ids, group_ids):
        memberships = []

        for student_id in student_ids:
            num_groups = random.randint(1, 3)
            assigned_groups = random.sample(group_ids, min(num_groups, len(group_ids)))

            for group_id in assigned_groups:
                memberships.append((student_id, group_id))

        query = """
            INSERT INTO STUDENTS_COURSE_GROUP_STUDENTS (STUDENT_ID, GROUP_ID)
            VALUES (%s, %s)
        """

        batch_size = 5000
        for i in range(0, len(memberships), batch_size):
            batch = memberships[i:i+batch_size]
            self.executemany(query, batch)

    def seed_schedule(self, courses, instructor_ids, group_ids, room_ids):
        schedules = []
        course_ids = list(courses.values())
        week_days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']
        lesson_ids = [1, 2, 3, 4, 5, 6]

        self.cursor.execute("SELECT INSTRUCTOR_ID, COURSE_ID FROM INSTRUCTORS_COURSES")
        valid_pairs = self.cursor.fetchall()
        self.conn.commit()

        if not valid_pairs:
            return

        target_schedules = NUM_SCHEDULES
        created = 0

        while created < target_schedules:
            instructor_id, course_id = random.choice(valid_pairs)
            group_id = random.choice(group_ids)
            week_day = random.choice(week_days)
            lesson_id = random.choice(lesson_ids)
            room_id = random.choice(room_ids)

            schedules.append((
                course_id,
                instructor_id,
                group_id,
                week_day,
                lesson_id,
                room_id
            ))

            created += 1

            if len(schedules) >= 10000:
                self._insert_schedule_batch(schedules)
                schedules = []

        if schedules:
            self._insert_schedule_batch(schedules)

    def _insert_schedule_batch(self, schedules):
        query = """
            INSERT INTO SCHEDULE (COURSE_ID, INSTRUCTOR_ID, STUDENTS_COURSE_GROUP_ID,
                                 WEEK_DAY, LESSON_SCHEDULE_ID, ROOM_ID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.executemany(query, schedules)

    def run(self):
        try:
            self.connect()
            self.clear_tables()

            self.seed_lessons_schedule()
            room_ids = self.seed_rooms()
            courses = self.seed_courses()
            instructor_ids = self.seed_instructors()
            self.seed_instructor_courses(instructor_ids, courses)
            student_ids = self.seed_students()
            group_ids = self.seed_student_course_groups(courses)
            self.seed_student_group_membership(student_ids, group_ids)
            self.seed_schedule(courses, instructor_ids, group_ids, room_ids)

        except Exception:
            import traceback
            traceback.print_exc()
            raise
        finally:
            self.disconnect()


if __name__ == '__main__':
    seeder = DatabaseSeeder()
    seeder.run()