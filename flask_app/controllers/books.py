from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.book import Book

@app.route('/books')
def show_books():
    book_data = Book.get_all()
    return render_template('books.html',title='Books',books=book_data)

@app.route('/books/new', methods=['POST'])
def add_book():
    data = {
        'title': request.form.get('title'),
        'num_of_pages': request.form.get('num_of_pages')
    }
    Book.add(data)
    return redirect('/books')

@app.route('/books/<int:book_id>')
def show_book(book_id):
    data = {
        'id': book_id
    }
    book_data = Book.get_one(data)
    return render_template('show_book.html',title='Show Book',book=book_data[0],unfavorites=book_data[1])

@app.route('/books/<int:book_id>/favorite', methods=['POST'])
def add_book_fav(book_id):
    data = {
        'bookId': book_id,
        'authorId': request.form.get('author')
    }
    Book.favorite(data)
    return redirect(f'/books/{book_id}')