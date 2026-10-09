# Smart Library Management System

> **Infographic:** Gemini image generation is unavailable in this environment. Generate one 16:9 infographic separately and save it as `assets/library-project-overview.png`; then place `![Smart Library Management System Project Overview](assets/library-project-overview.png)` above this heading.

A command-line library system built with Python 3.9+ and SQLite. It manages books, students, circulation, availability, and complete borrowing history while persisting data in `library.db`.

## Problem and objectives

Manual library records make it difficult to know which books are available, prevent duplicate loans, and preserve reliable borrowing history. This project provides a small, dependable system that:

- Maintains unique book and student records.
- Issues books only to registered students.
- Prevents more than one active loan for a book.
- Records issue and return dates for reporting and accountability.
- Validates invalid input without crashing.

## Features and requirements

- Add, list, and search books by unique ID or partial title.
- Register and list students by unique ID.
- Issue books to registered students and return active loans.
- Show available books and currently borrowed books with student details.
- Show complete borrowing history for a student, including returned loans.
- Use parameterized SQL, SQLite foreign keys, transactions, and a partial unique index for active loans.
- Create the database schema automatically when the application starts.

## Technology stack

- **Language:** Python 3.9+
- **Database:** SQLite via Python's standard-library `sqlite3` module
- **Interface:** Command-line interface
- **Testing:** `unittest`
- **Dependencies:** None outside the Python standard library

## Project structure

```text
smart-library-management/
├── main.py
├── database.py
├── library.py
├── models.py
├── reports.py
├── tests/
│   ├── __init__.py
│   └── test_library.py
├── README.md
└── requirements.txt
```

When the infographic is generated, add `assets/library-project-overview.png` to the project as described at the top of this file.

## Installation and execution

No package installation is required. From the repository root:

```bash
cd smart-library-management
python main.py
```

The application creates `library.db` and its tables automatically. The database file is persistent and survives application restarts.

## Command-line menu

```text
1. Add New Book
2. View All Books
3. Search Book
4. Register Student
5. View All Students
6. Issue Book
7. Return Book
8. View Available Books
9. View Borrowed Books
10. Student Borrowing History
11. Exit
```

## Database design

### Books

Stores `book_id` as a unique primary key and the book `title`.

### Students

Stores `student_id` as a unique primary key and the student's `name`.

### Borrowing

Stores each loan with an auto-generated `borrowing_id`, foreign-key references to `book_id` and `student_id`, an `issue_date`, and a nullable `return_date`. A loan is active while `return_date IS NULL`. A SQLite partial unique index enforces at most one active borrowing record per book. Returned records remain in the table, preserving history and making a book available again.

## Testing

Run the complete test suite from the project directory:

```bash
python -m unittest discover -s tests -v
```

The tests cover successful book and student creation, duplicate IDs, searching, valid issue and return operations, unavailable books, unknown books and students, invalid returns, borrowing history, foreign keys, and availability after return. Temporary databases are used so tests never modify the real `library.db`.

## Agile methodology application

- **XP:** Test-driven development, unit testing, small increments, refactoring, and frequent integration support fast feedback and maintainable code.
- **FDD:** A feature list organizes incremental implementation around book management, student management, circulation, availability, and reports.
- **DSDM:** MoSCoW prioritization puts essential circulation and data integrity first, with user involvement and short timeboxed delivery.
- **Crystal:** Teamwork, communication, role allocation, code reviews, and frequent delivery keep the project lightweight and responsive.

These practices describe how the project can be developed and reviewed; no single Python function implements an Agile methodology.

## Expected outcomes and limitations

The system provides reliable small-library circulation, persistent records, useful reports, and repeatable automated tests through a simple terminal interface. It is intended for a single local user and does not provide authentication, multi-user concurrency management beyond SQLite transactions, a graphical/web interface, barcode scanning, overdue notifications, or deployment infrastructure.