# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import Library, Book, Member

app = Flask(__name__)
app.secret_key = "replace-with-a-secret-key"  # for flash messages

library = Library()  

@app.route("/")
def index():
    total_books = sum(b.available_copies for b in library.books)
    total_titles = len(library.books)
    total_members = len(library.members)
    borrowed_count = sum(len(m.borrowed_books) for m in library.members)
    return render_template("index.html",
                           total_books=total_books,
                           total_titles=total_titles,
                           total_members=total_members,
                           borrowed_count=borrowed_count)

# ----- Books -----
@app.route("/books")
def books():
    return render_template("books.html", books=library.books)

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = request.form["book_id"].strip()
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        copies = request.form["copies"].strip()
        if not (book_id and title and author and copies.isdigit()):
            flash("Please provide valid book details.", "danger")
            return redirect(url_for("add_book"))
        library.add_book(Book(book_id, title, author, int(copies)))
        flash(f"Book {title}  added successfully!", "success")
        return redirect(url_for("books"))
    return render_template("add_book.html")

# ----- Members -----
@app.route("/members")
def members():
    return render_template("members.html", members=library.members)

@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        member_id = request.form["member_id"].strip()
        name = request.form["name"].strip()
        if not (member_id and name):
            flash("Please provide valid member details.", "danger")
            return redirect(url_for("add_member"))
        success = library.add_member(Member(member_id, name))
        if success:
            flash(f"Member {name} added.", "success")
            return redirect(url_for("members"))
        else:
            flash("Member ID already exists.", "warning")
            return redirect(url_for("add_member"))
    return render_template("add_member.html")

# ----- Transactions -----
@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        typ = request.form.get("type")
        member_id = request.form.get("member_id").strip()
        book_title = request.form.get("book_title").strip()
        if typ == "borrow":
            success, msg = library.borrow_transaction(member_id, book_title)
        else:
            success, msg = library.return_transaction(member_id, book_title)

        flash(msg, "success" if success else "danger")
        return redirect(url_for("transactions"))

    return render_template("transactions.html", members=library.members, books=library.books)

if __name__ == "__main__":
    app.run(debug=True)
