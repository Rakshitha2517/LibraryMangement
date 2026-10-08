import pytest

from app import database, library


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Each test gets a fresh empty database file."""
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()


def test_add_and_list():
    library.add_book("Clean Code", "Robert Martin")
    books = library.list_books()
    assert len(books) == 1
    assert books[0]["title"] == "Clean Code"


def test_empty_title_rejected():
    with pytest.raises(ValueError):
        library.add_book("  ", "Someone")


def test_search():
    library.add_book("Python Basics", "Guido")
    library.add_book("Java Basics", "James")
    assert len(library.search_books("python")) == 1


def test_issue_and_return():
    book_id = library.add_book("DevOps Handbook", "Gene Kim")
    library.issue_book(book_id, "Rakshi")
    assert library.list_books()[0]["issued_to"] == "Rakshi"
    library.return_book(book_id)
    assert library.list_books()[0]["issued_to"] is None


def test_cannot_issue_twice():
    book_id = library.add_book("SQL Guide", "Author")
    library.issue_book(book_id, "A")
    with pytest.raises(ValueError):
        library.issue_book(book_id, "B")


def test_delete_missing_book():
    with pytest.raises(ValueError):
        library.delete_book(999)
