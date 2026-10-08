"""Console menu. Run with:  python -m app.main"""
from app import library
from app.database import init_db

MENU = """
===== LIBRARY MANAGEMENT =====
1. Add book
2. List all books
3. Search book
4. Issue book
5. Return book
6. Delete book
0. Exit
"""


def print_books(books):
    if not books:
        print("No books found.")
        return
    print(f"{'ID':<4}{'TITLE':<30}{'AUTHOR':<20}STATUS")
    for b in books:
        status = f"Issued to {b['issued_to']} on {b['issue_date']}" if b["issued_to"] else "Available"
        print(f"{b['id']:<4}{b['title']:<30}{b['author']:<20}{status}")


def read_id(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("ID must be a number.")
    return int(value)


def main():
    init_db()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                book_id = library.add_book(input("Title: "), input("Author: "))
                print(f"Book added with ID {book_id}.")
            elif choice == "2":
                print_books(library.list_books())
            elif choice == "3":
                print_books(library.search_books(input("Keyword: ")))
            elif choice == "4":
                library.issue_book(read_id("Book ID: "), input("Student name: "))
                print("Book issued.")
            elif choice == "5":
                library.return_book(read_id("Book ID: "))
                print("Book returned.")
            elif choice == "6":
                library.delete_book(read_id("Book ID: "))
                print("Book deleted.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again.")
        except ValueError as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    main()
