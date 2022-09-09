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