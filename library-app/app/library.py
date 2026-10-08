"""Business logic: add, list, search, issue, return, delete books."""
from contextlib import closing
from datetime import date

from app.database import get_connection


def add_book(title, author):
    title, author = title.strip(), author.strip()
    if not title or not author:
        raise ValueError("Title and author cannot be empty.")
    with closing(get_connection()) as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author) VALUES (?, ?)", (title, author)
        )
        conn.commit()
        return cur.lastrowid


def list_books():
    with closing(get_connection()) as conn:
        return conn.execute("SELECT * FROM books ORDER BY id").fetchall()


def search_books(keyword):
    like = f"%{keyword.strip()}%"
    with closing(get_connection()) as conn:
        return conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (like, like)
        ).fetchall()


def _get_book(conn, book_id):
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    if book is None:
        raise ValueError(f"No book with id {book_id}.")
    return book


def issue_book(book_id, student_name):
    student_name = student_name.strip()
    if not student_name:
        raise ValueError("Student name cannot be empty.")
    with closing(get_connection()) as conn:
        book = _get_book(conn, book_id)
        if book["issued_to"]:
            raise ValueError(f"Book already issued to {book['issued_to']}.")
        conn.execute(
            "UPDATE books SET issued_to = ?, issue_date = ? WHERE id = ?",
            (student_name, date.today().isoformat(), book_id),
        )
        conn.commit()


def return_book(book_id):
    with closing(get_connection()) as conn:
        book = _get_book(conn, book_id)
        if not book["issued_to"]:
            raise ValueError("This book is not issued.")
        conn.execute(
            "UPDATE books SET issued_to = NULL, issue_date = NULL WHERE id = ?",
            (book_id,),
        )
        conn.commit()


def delete_book(book_id):
    with closing(get_connection()) as conn:
        _get_book(conn, book_id)
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
