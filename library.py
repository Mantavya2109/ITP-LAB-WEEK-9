from datetime import date
import sqlite3

from database import get_connection
from models import Book, Student


class LibraryError(Exception):
    pass


def _required(value, label):
    value = str(value).strip()
    if not value:
        raise LibraryError(f"{label} cannot be empty.")
    return value


def add_book(db_path, book_id, title):
    book_id, title = _required(book_id, "Book ID"), _required(title, "Title")
    try:
        with get_connection(db_path) as connection:
            connection.execute("INSERT INTO books(book_id, title) VALUES (?, ?)", (book_id, title))
    except sqlite3.IntegrityError as error:
        raise LibraryError("Book ID already exists.") from error
    return Book(book_id, title)


def list_books(db_path):
    with get_connection(db_path) as connection:
        return [Book(row["book_id"], row["title"]) for row in connection.execute(
            "SELECT book_id, title FROM books ORDER BY book_id")]


def search_books(db_path, query):
    query = _required(query, "Search term")
    with get_connection(db_path) as connection:
        rows = connection.execute(
            "SELECT book_id, title FROM books WHERE book_id = ? OR title LIKE ? ORDER BY book_id",
            (query, f"%{query}%"),
        )
        return [Book(row["book_id"], row["title"]) for row in rows]


def register_student(db_path, student_id, name):
    student_id, name = _required(student_id, "Student ID"), _required(name, "Name")
    try:
        with get_connection(db_path) as connection:
            connection.execute("INSERT INTO students(student_id, name) VALUES (?, ?)", (student_id, name))
    except sqlite3.IntegrityError as error:
        raise LibraryError("Student ID already exists.") from error
    return Student(student_id, name)


def list_students(db_path):
    with get_connection(db_path) as connection:
        return [Student(row["student_id"], row["name"]) for row in connection.execute(
            "SELECT student_id, name FROM students ORDER BY student_id")]


def issue_book(db_path, book_id, student_id, issue_date=None):
    book_id, student_id = _required(book_id, "Book ID"), _required(student_id, "Student ID")
    issue_date = issue_date or date.today().isoformat()
    try:
        with get_connection(db_path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            if connection.execute("SELECT 1 FROM books WHERE book_id = ?", (book_id,)).fetchone() is None:
                raise LibraryError("Book not found.")
            if connection.execute("SELECT 1 FROM students WHERE student_id = ?", (student_id,)).fetchone() is None:
                raise LibraryError("Student not found.")
            if connection.execute(
                "SELECT 1 FROM borrowings WHERE book_id = ? AND return_date IS NULL", (book_id,)
            ).fetchone() is not None:
                raise LibraryError("Book is already borrowed.")
            connection.execute(
                "INSERT INTO borrowings(book_id, student_id, issue_date) VALUES (?, ?, ?)",
                (book_id, student_id, issue_date),
            )
    except sqlite3.IntegrityError as error:
        raise LibraryError("Book is already borrowed.") from error


def return_book(db_path, book_id, return_date=None):
    book_id = _required(book_id, "Book ID")
    return_date = return_date or date.today().isoformat()
    with get_connection(db_path) as connection:
        result = connection.execute(
            "UPDATE borrowings SET return_date = ? WHERE book_id = ? AND return_date IS NULL",
            (return_date, book_id),
        )
        if result.rowcount == 0:
            raise LibraryError("No active borrowing found for this book.")