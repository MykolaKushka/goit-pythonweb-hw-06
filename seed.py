import random
from faker import Faker
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Group, Student, Teacher, Subject, Grade
from datetime import datetime

fake = Faker()
db = SessionLocal()

# Create 3 student groups
def create_groups():
    groups = []
    for i in range(1, 4):
        group = Group(name=f"Group {i}")
        db.add(group)
        groups.append(group)
    db.commit()
    return groups

# Create 50 students and assign them to random groups
def create_students(groups):
    students = []
    for _ in range(50):
        group = random.choice(groups)
        student = Student(name=fake.name(), group=group)
        db.add(student)
        students.append(student)
    db.commit()
    return students

# Create 4 teachers with random names
def create_teachers():
    teachers = []
    for _ in range(4):
        teacher = Teacher(name=fake.name())
        db.add(teacher)
        teachers.append(teacher)
    db.commit()
    return teachers

# Create 5 to 8 subjects and assign each to a random teacher
def create_subjects(teachers):
    subjects = []
    subject_names = [
        "Math", "History", "Physics", "Biology",
        "Chemistry", "Literature", "Geography", "English"
    ]
    for name in subject_names[:random.randint(5, 8)]:
        teacher = random.choice(teachers)
        subject = Subject(name=name, teacher=teacher)
        db.add(subject)
        subjects.append(subject)
    db.commit()
    return subjects

# Assign 10 to 20 grades to each student for each subject
def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(10, 20)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.randint(60, 100),
                    date_received=fake.date_between(start_date='-1y', end_date='today')
                )
                db.add(grade)
    db.commit()

# Run all seed functions
def seed_data():
    print("🌱 Seeding database...")
    groups = create_groups()
    students = create_students(groups)
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    create_grades(students, subjects)
    print("✅ Done!")

# Entry point of the script
if __name__ == "__main__":
    seed_data()
    db.close()
