from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    book_id: str
    title: str


@dataclass(frozen=True)
class Student:
    student_id: str
    name: str