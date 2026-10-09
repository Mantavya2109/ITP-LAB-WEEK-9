from database import initialize_database
from library import (LibraryError, add_book, issue_book, list_books, list_students,
                      register_student, return_book, search_books)
from reports import (print_available_books, print_borrowed_books, print_history)


MENU = """\n1. Add New Book
2. View All Books
3. Search Book
4. Register Student
5. View All Students
6. Issue Book
7. Return Book
8. View Available Books
9. View Borrowed Books
10. Student Borrowing History
11. Exit"""


def show_items(items, formatter):
    print("No records found." if not items else "\n".join(formatter(item) for item in items))


def run(db_path="library.db"):
    initialize_database(db_path)
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_book(db_path, input("Book ID: "), input("Title: "))
                print("Book added.")
            elif choice == "2":
                show_items(list_books(db_path), lambda book: f"{book.book_id}: {book.title}")
            elif choice == "3":
                show_items(search_books(db_path, input("Book ID or title: ")), lambda book: f"{book.book_id}: {book.title}")
            elif choice == "4":
                register_student(db_path, input("Student ID: "), input("Name: "))
                print("Student registered.")
            elif choice == "5":
                show_items(list_students(db_path), lambda student: f"{student.student_id}: {student.name}")
            elif choice == "6":
                issue_book(db_path, input("Book ID: "), input("Student ID: "))
                print("Book issued.")
            elif choice == "7":
                return_book(db_path, input("Book ID: "))
                print("Book returned.")
            elif choice == "8":
                print_available_books(db_path)
            elif choice == "9":
                print_borrowed_books(db_path)
            elif choice == "10":
                print_history(db_path, input("Student ID: "))
            elif choice == "11":
                print("Goodbye.")
                break
            else:
                print("Invalid menu choice.")
        except LibraryError as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    run()