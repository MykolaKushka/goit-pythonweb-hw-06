from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

# Represents a student group (e.g., "Group A", "Group 1", etc.)
class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # One-to-many relationship with Student
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


# Represents a student who belongs to a group and receives grades
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    # Many-to-one relationship with Group
    group: Mapped["Group"] = relationship("Group", back_populates="students")

    # One-to-many relationship with Grade
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


# Represents a teacher who teaches one or more subjects
class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # One-to-many relationship with Subject
    subjects: Mapped[list["Subject"]] = relationship("Subject", back_populates="teacher")


# Represents a subject taught by a teacher
class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    # Many-to-one relationship with Teacher
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")

    # One-to-many relationship with Grade
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")


# Represents a grade that a student received for a specific subject
class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(nullable=False)
    date_received: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Many-to-one relationship with Student
    student: Mapped["Student"] = relationship("Student", back_populates="grades")

    # Many-to-one relationship with Subject
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")
