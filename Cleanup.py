import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(credentials.env)  

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()
print("Dropping trigger...")
cursor.execute("DROP TRIGGER IF EXISTS schedule_room_capacity_trigger ON SCHEDULE")

print("Dropping function...")
cursor.execute("DROP FUNCTION IF EXISTS check_room_capacity()")

print("Clearing SCHEDULE...")
cursor.execute("DELETE FROM SCHEDULE")

print("Clearing STUDENTS_COURSE_GROUP_STUDENTS...")
cursor.execute("DELETE FROM STUDENTS_COURSE_GROUP_STUDENTS")

print("Clearing STUDENTS_COURSE_GROUPS...")
cursor.execute("DELETE FROM STUDENTS_COURSE_GROUPS")

print("Clearing INSTRUCTORS_COURSES...")
cursor.execute("DELETE FROM INSTRUCTORS_COURSES")

print("Clearing STUDENTS...")
cursor.execute("DELETE FROM STUDENTS")

print("Clearing INSTRUCTORS...")
cursor.execute("DELETE FROM INSTRUCTORS")

print("Clearing COURSES...")
cursor.execute("DELETE FROM COURSES")

conn.commit()
cursor.close()
conn.close()

print("Done!")