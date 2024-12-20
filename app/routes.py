from datetime import datetime

from app.models import User, Book, BorrowHistory
from flask import current_app as app, render_template, flash
from flask import render_template, request, redirect, url_for
from app import create_app, db
from app.models import Book
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

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

@app.route('/books')
def view_books():
    books = Book.query.all()
    borrow_history = BorrowHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('books.html', books=books, borrow_history=borrow_history)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        quantity = request.form['quantity']
        new_book = Book(title=title, author=author, isbn=isbn, quantity=quantity)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('books'))
    return render_template('add_books.html')

@app.route('/books/delete/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'danger')
    return redirect(url_for('books'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.quantity = request.form['quantity']
        db.session.commit()
        flash('Book details updated successfully!', 'success')
        return redirect(url_for('books'))
    return render_template('edit_book.html', book=book)

@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.quantity > 0:
        due_date = datetime.datetime.now() + datetime.timedelta(days=14)
        borrow_history = BorrowHistory(
            book_id=book.id,
            user_id=current_user.id,
            borrow_date=datetime.datetime.now(),
            due_date=due_date
        )
        book.quantity -= 1
        db.session.add(borrow_history)
        db.session.commit()
    return redirect(url_for('view_books'))

@app.route('/return/<int:borrow_id>', methods=['POST'])
@login_required
def return_book(borrow_id):
    borrow_history = BorrowHistory.query.get_or_404(borrow_id)
    book = Book.query.get(borrow_history.book_id)
    if not borrow_history.returned:
        borrow_history.return_date = datetime.datetime.now()
        borrow_history.returned = True
        book.quantity += 1
        if borrow_history.return_date > borrow_history.due_date:
            borrow_history.late_fee = (borrow_history.return_date - borrow_history.due_date).days * 1.0
        db.session.commit()
    return redirect(url_for('view_books'))

@app.route('/report/most_borrowed')
@login_required
def most_borrowed():
    reports = db.session.query(
        Book.title,
        db.func.count(BorrowHistory.id).label('borrow_count')
    ).join(BorrowHistory).group_by(Book.title).order_by(db.desc('borrow_count')).all()
    return render_template('report.html', reports=reports)
