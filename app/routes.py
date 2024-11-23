from app.models import User, Book
from flask import current_app as app, render_template
from flask import render_template, request, redirect, url_for
from app import create_app, db
from app.models import Book

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('users'))

@app.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/books', methods=['GET'])
def view_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = int(request.form['quantity'])

        new_book = Book(title=title, author=author, isbn=isbn, quantity=quantity)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('view_books'))
    return render_template('add_book.html')