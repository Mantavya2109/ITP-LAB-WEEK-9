import os
import tempfile
import unittest

from database import initialize_database, get_connection
from library import (LibraryError, add_book, issue_book, list_books, register_student,
                      return_book, search_books)
from reports import available_books, borrowing_history, borrowed_books


class LibraryTests(unittest.TestCase):
    def setUp(self):
        handle, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        initialize_database(self.db_path)

    def tearDown(self):
        os.remove(self.db_path)

    def seed(self):
        add_book(self.db_path, "B1", "Python Basics")
        add_book(self.db_path, "B2", "SQLite Guide")
        register_student(self.db_path, "S1", "Asha")

    def test_creation_duplicates_and_search(self):
        self.seed()
        self.assertEqual(len(list_books(self.db_path)), 2)
        self.assertEqual([book.book_id for book in search_books(self.db_path, "python")], ["B1"])
        with self.assertRaises(LibraryError):
            add_book(self.db_path, "B1", "Other")
        with self.assertRaises(LibraryError):
            register_student(self.db_path, "S1", "Other")

    def test_issue_return_history_and_availability(self):
        self.seed()
        issue_book(self.db_path, "B1", "S1", "2026-01-01")
        self.assertEqual(len(borrowed_books(self.db_path)), 1)
        self.assertEqual([book["book_id"] for book in available_books(self.db_path)], ["B2"])
        with self.assertRaises(LibraryError):
            issue_book(self.db_path, "B1", "S1")
        return_book(self.db_path, "B1", "2026-01-02")
        history = borrowing_history(self.db_path, "S1")
        self.assertEqual(history[0]["return_date"], "2026-01-02")
        self.assertEqual([book["book_id"] for book in available_books(self.db_path)], ["B1", "B2"])

    def test_unknown_and_invalid_requests(self):
        self.seed()
        with self.assertRaises(LibraryError):
            issue_book(self.db_path, "missing", "S1")
        with self.assertRaises(LibraryError):
            issue_book(self.db_path, "B1", "missing")
        with self.assertRaises(LibraryError):
            return_book(self.db_path, "B1")
        with self.assertRaises(LibraryError):
            add_book(self.db_path, "", "Title")

    def test_foreign_keys_are_enabled(self):
        with get_connection(self.db_path) as connection:
            self.assertEqual(connection.execute("PRAGMA foreign_keys").fetchone()[0], 1)


if __name__ == "__main__":
    unittest.main()