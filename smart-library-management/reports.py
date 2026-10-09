from database import get_connection


def available_books(db_path):
    with get_connection(db_path) as connection:
        return connection.execute("""
            SELECT b.book_id, b.title FROM books b
            WHERE NOT EXISTS (SELECT 1 FROM borrowings r
                              WHERE r.book_id = b.book_id AND r.return_date IS NULL)
            ORDER BY b.book_id
        """).fetchall()


def borrowed_books(db_path):
    with get_connection(db_path) as connection:
        return connection.execute("""
            SELECT b.book_id, b.title, s.student_id, s.name, r.issue_date
            FROM borrowings r
            JOIN books b ON b.book_id = r.book_id
            JOIN students s ON s.student_id = r.student_id
            WHERE r.return_date IS NULL ORDER BY b.book_id
        """).fetchall()


def borrowing_history(db_path, student_id):
    with get_connection(db_path) as connection:
        return connection.execute("""
            SELECT b.book_id, b.title, r.issue_date, r.return_date
            FROM borrowings r JOIN books b ON b.book_id = r.book_id
            WHERE r.student_id = ? ORDER BY r.issue_date, r.borrowing_id
        """, (student_id.strip(),)).fetchall()


def print_available_books(db_path):
    rows = available_books(db_path)
    print("No available books." if not rows else "\n".join(f"{row['book_id']}: {row['title']}" for row in rows))


def print_borrowed_books(db_path):
    rows = borrowed_books(db_path)
    print("No borrowed books." if not rows else "\n".join(
        f"{row['book_id']}: {row['title']} | {row['student_id']} - {row['name']} | Issued {row['issue_date']}"
        for row in rows
    ))


def print_history(db_path, student_id):
    rows = borrowing_history(db_path, student_id)
    print("No borrowing history." if not rows else "\n".join(
        f"{row['book_id']}: {row['title']} | {row['issue_date']} to {row['return_date'] or 'active'}"
        for row in rows
    ))