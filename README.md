  Smart Library Management System (Flask + Python OOP)

A Smart Library Management System built using **Flask**, **Python OOP principles**, and **file-based data persistence**.  
The system allows librarians to manage books, members, and borrowing transactions efficiently.
##  Features
  Add, view, and manage **Books**  
  Register and list **Members**  
  Borrow and return books  
  Tracks and displays the **most borrowed book**  
  Generates a **transaction history report**  
   **Search books by author**  
  Data persistence via `books.txt` and `members.txt`  
  Modern and responsive UI using HTML + CSS + Flask templates  

---

## Object-Oriented Concepts Applied
- **Encapsulation** – Data attributes are managed via class methods  
- **Inheritance** – Logical relationships and reusable class design  
- **Polymorphism** – Flexible method usage for books and members  
- **Abstraction** – Simplified user interaction through menus/UI  

---

## Class Design
### `Book`
- Attributes: `book_id`, `title`, `author`, `available_copies`
- Methods: `display_info()`, `update_copies()`

### `Member`
- Attributes: `member_id`, `name`, `borrowed_books`
- Methods: `borrow_book()`, `return_book()`, `display_member_info()`

### `Library`
- Attributes: `books`, `members`
- Methods:  
  `add_book()`, `add_member()`,  
  `display_all_books()`, `display_all_members()`,  
  `borrow_transaction()`, `return_transaction()`



File Handling
Data is saved and loaded from:
- `books.txt`
- `members.txt`

All updates persist even after restarting the application.

---

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/collinskiprotich892-star/smart_library_flask.git
   cd smart_library_flask
