# models.py
import os
import json

class Book:  #class book
    def __init__(self, book_id, title, author, available_copies):
        self.book_id = str(book_id)
        self.title = title
        self.author = author
        self.available_copies = int(available_copies)

    def display_info(self):
        return f"ID: {self.book_id} | {self.title} by {self.author} ({self.available_copies} copies)"

    def update_copies(self, number):
        self.available_copies = int(self.available_copies) + int(number)

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "available_copies": self.available_copies
        }

class Member: #class member
    def __init__(self, member_id, name, borrowed_books=None):
        self.member_id = str(member_id)
        self.name = name
        self.borrowed_books = borrowed_books or []  # list of titles

    def borrow_book(self, book: Book):
        if book.available_copies > 0:
            book.update_copies(-1)
            self.borrowed_books.append(book.title)
            return True, f"{self.name} borrowed '{book.title}'."
        return False, f"'{book.title}' is not available."

    def return_book(self, book: Book):
        if book.title in self.borrowed_books:
            book.update_copies(1)
            self.borrowed_books.remove(book.title)
            return True, f"{self.name} returned '{book.title}'."
        return False, f"{self.name} has not borrowed '{book.title}'."

    def display_member_info(self):
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        return f"Member ID: {self.member_id} | {self.name} | Borrowed: {borrowed}"

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books
        }

class Library: #class library
    BOOKS_FILE = "books.txt"
    MEMBERS_FILE = "members.txt"

    def __init__(self):
        self.books = []
        self.members = []
        self.load_data()

    # Book/member management
    def add_book(self, book: Book):
        # it avoid duplicate IDs e.g. if same id exists, it update copies
        existing = self.find_book_by_id(book.book_id)
        if existing:
            existing.update_copies(book.available_copies)
        else:
            self.books.append(book)
        self.save_data()

    def add_member(self, member: Member):
        if self.find_member_by_id(member.member_id):
            return False
        self.members.append(member)
        self.save_data()
        return True

    def find_book_by_title(self, title):
        return next((b for b in self.books if b.title.lower() == title.lower()), None)

    def find_book_by_id(self, book_id):
        return next((b for b in self.books if b.book_id == str(book_id)), None)

    def find_member_by_id(self, member_id):
        return next((m for m in self.members if m.member_id == str(member_id)), None)

    def borrow_transaction(self, member_id, book_title):
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)
        if not member:
            return False, "Member not found."
        if not book:
            return False, "Book not found."
        success, msg = member.borrow_book(book)
        if success:
            self.save_data()
        return success, msg

    def return_transaction(self, member_id, book_title):
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_title(book_title)
        if not member:
            return False, "Member not found."
        if not book:
            return False, "Book not found."
        success, msg = member.return_book(book)
        if success:
            self.save_data()
        return success, msg

    # Persistence
    def save_data(self):
        with open(self.BOOKS_FILE, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=2)
        with open(self.MEMBERS_FILE, "w") as f:
            json.dump([m.to_dict() for m in self.members], f, indent=2)

    def load_data(self):
        # load books
        if os.path.exists(self.BOOKS_FILE):
            try:
                with open(self.BOOKS_FILE, "r") as f:
                    books_data = json.load(f)
                    self.books = [Book(**b) for b in books_data]
            except Exception:
                self.books = []

        # load members
        if os.path.exists(self.MEMBERS_FILE):
            try:
                with open(self.MEMBERS_FILE, "r") as f:
                    members_data = json.load(f)
                    self.members = [Member(m["member_id"], m["name"], m.get("borrowed_books", [])) for m in members_data]
            except Exception:
                self.members = []
