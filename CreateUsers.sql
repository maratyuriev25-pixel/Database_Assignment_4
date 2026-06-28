-- ============================================================================
-- USER 1: ADMIN USER - Full administrative access
-- ============================================================================

DROP USER IF EXISTS admin_user;
CREATE USER admin_user WITH PASSWORD 'admin_secure_pass_123';

GRANT CONNECT ON DATABASE postgres TO admin_user;
GRANT USAGE ON SCHEMA public TO admin_user;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin_user;

-- ============================================================================
-- USER 2: FACULTY USER - For instructors
-- ============================================================================

DROP USER IF EXISTS faculty_user;
CREATE USER faculty_user WITH PASSWORD 'faculty_secure_pass_456';

GRANT CONNECT ON DATABASE postgres TO faculty_user;
GRANT USAGE ON SCHEMA public TO faculty_user;

GRANT SELECT ON COURSES TO faculty_user;
GRANT SELECT ON ROOMS TO faculty_user;
GRANT SELECT ON LESSONS_SCHEDULE TO faculty_user;

GRANT SELECT, UPDATE ON INSTRUCTORS TO faculty_user;
GRANT SELECT ON INSTRUCTORS_COURSES TO faculty_user;

GRANT SELECT ON SCHEDULE TO faculty_user;
GRANT SELECT ON STUDENTS TO faculty_user;
GRANT SELECT ON STUDENTS_COURSE_GROUPS TO faculty_user;
GRANT SELECT ON STUDENTS_COURSE_GROUP_STUDENTS TO faculty_user;

GRANT SELECT ON INSTRUCTOR_SCHEDULE TO faculty_user;
GRANT SELECT ON STUDENT_SCHEDULE TO faculty_user;
GRANT SELECT ON COURSE_STATISTICS TO faculty_user;

GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO faculty_user;

-- ============================================================================
-- USER 3: STUDENT USER - For students
-- ============================================================================

DROP USER IF EXISTS student_user;
CREATE USER student_user WITH PASSWORD 'student_secure_pass_789';

GRANT CONNECT ON DATABASE postgres TO student_user;
GRANT USAGE ON SCHEMA public TO student_user;

GRANT SELECT ON COURSES TO student_user;
GRANT SELECT ON ROOMS TO student_user;
GRANT SELECT ON LESSONS_SCHEDULE TO student_user;
GRANT SELECT ON INSTRUCTORS TO student_user;

GRANT SELECT ON STUDENTS TO student_user;
GRANT SELECT ON STUDENTS_COURSE_GROUPS TO student_user;
GRANT SELECT ON STUDENTS_COURSE_GROUP_STUDENTS TO student_user;
GRANT SELECT ON SCHEDULE TO student_user;

GRANT SELECT ON STUDENT_SCHEDULE TO student_user;
GRANT SELECT ON COURSE_STATISTICS TO student_user;

GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO student_user;

-- ============================================================================
-- USER 4: AUDIT USER - For compliance and monitoring
-- ============================================================================

DROP USER IF EXISTS audit_user;
CREATE USER audit_user WITH PASSWORD 'audit_secure_pass_012';

GRANT CONNECT ON DATABASE postgres TO audit_user;
GRANT USAGE ON SCHEMA public TO audit_user;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO audit_user;

GRANT SELECT ON STUDENT_SCHEDULE TO audit_user;
GRANT SELECT ON INSTRUCTOR_SCHEDULE TO audit_user;
GRANT SELECT ON COURSE_STATISTICS TO audit_user;
GRANT SELECT ON ROOM_UTILIZATION TO audit_user;
GRANT SELECT ON INACTIVE_USERS TO audit_user;
GRANT SELECT ON AUDIT_LOG TO audit_user;

GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO audit_user;


ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO student_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO faculty_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO audit_user;
