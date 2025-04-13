from app.db import SessionLocal
from app.models import Student, Subject, Teacher, Grade, Group
from sqlalchemy import func

def print_section(title):
    print(f"\n{'=' * 40}\n{title}\n{'=' * 40}")

db = SessionLocal()

# 1. Top 5 students by average grade
print_section("1. Top 5 students by average grade")
q1 = (
    db.query(Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
    .join(Grade)
    .group_by(Student.id)
    .order_by(func.avg(Grade.grade).desc())
    .limit(5)
    .all()
)
for row in q1:
    print(row)

# 2. Student with highest average in a specific subject
print_section("2. Top student by average grade in subject 'Math'")
subject_name = "Math"
q2 = (
    db.query(Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
    .join(Grade)
    .join(Subject)
    .filter(Subject.name == subject_name)
    .group_by(Student.id)
    .order_by(func.avg(Grade.grade).desc())
    .limit(1)
    .first()
)
print(q2)

# 3. Average grade in each group for a specific subject
print_section("3. Average grade per group in subject 'Math'")
q3 = (
    db.query(Group.name, func.round(func.avg(Grade.grade), 2))
    .select_from(Grade)
    .join(Student, Student.id == Grade.student_id)
    .join(Group, Group.id == Student.group_id)
    .join(Subject, Subject.id == Grade.subject_id)
    .filter(Subject.name == subject_name)
    .group_by(Group.id)
    .all()
)
for row in q3:
    print(row)

# 4. Average grade across all subjects and students
print_section("4. Average grade across all grades")
q4 = db.query(func.round(func.avg(Grade.grade), 2)).scalar()
print(q4)

# 5. Subjects taught by a specific teacher
print_section("5. Subjects taught by teacher 'Dr. John Smith'")
teacher_name = "Dr. John Smith"
q5 = db.query(Subject.name).join(Teacher).filter(Teacher.name == teacher_name).all()
for row in q5:
    print(row)

# 6. List of students in a specific group
print_section("6. Students in group 'Group A'")
group_name = "Group A"
q6 = db.query(Student.name).join(Group).filter(Group.name == group_name).all()
for row in q6:
    print(row)

# 7. Grades in a subject for students of a specific group
print_section("7. Grades in 'Math' for group 'Group A'")
q7 = (
    db.query(Student.name, Grade.grade)
    .join(Grade)
    .join(Group)
    .join(Subject)
    .filter(Group.name == group_name, Subject.name == subject_name)
    .all()
)
for row in q7:
    print(row)

# 8. Average grade each teacher gives in their subjects
print_section("8. Average grade per teacher")
q8 = (
    db.query(Teacher.name, func.round(func.avg(Grade.grade), 2))
    .select_from(Grade)
    .join(Subject, Subject.id == Grade.subject_id)
    .join(Teacher, Teacher.id == Subject.teacher_id)
    .group_by(Teacher.id)
    .all()
)
for row in q8:
    print(row)

# 9. List of subjects attended by a specific student
print_section("9. Courses attended by student 'Dennis Spears'")
student_name = "Dennis Spears"
q9 = (
    db.query(Subject.name)
    .join(Grade)
    .join(Student)
    .filter(Student.name == student_name)
    .distinct()
    .all()
)
for row in q9:
    print(row)

# 10. Subjects taught by a specific teacher to a specific student
print_section("10. Courses by 'Dr. John Smith' for student 'Dennis Spears'")
q10 = (
    db.query(Subject.name)
    .join(Grade)
    .join(Student)
    .join(Teacher)
    .filter(Student.name == student_name, Teacher.name == teacher_name)
    .distinct()
    .all()
)
for row in q10:
    print(row)

db.close()
