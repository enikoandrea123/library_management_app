CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('librarian', 'student')) NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    quantity INT NOT NULL DEFAULT 0
);

CREATE TABLE borrowed_books (
    user_id INT REFERENCES users(id),
    book_id INT REFERENCES books(id),
    borrow_date DATE DEFAULT CURRENT_DATE,
    return_date DATE
);
