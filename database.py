import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    book_id TEXT PRIMARY KEY,
    title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS borrowings (
    borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id TEXT NOT NULL REFERENCES books(book_id),
    student_id TEXT NOT NULL REFERENCES students(student_id),
    issue_date TEXT NOT NULL,
    return_date TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS one_active_borrowing_per_book
ON borrowings(book_id) WHERE return_date IS NULL;
"""


def get_connection(db_path="library.db"):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path="library.db"):
    with get_connection(db_path) as connection:
        connection.executescript(SCHEMA)