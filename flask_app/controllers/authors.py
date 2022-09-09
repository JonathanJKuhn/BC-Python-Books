from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.author import Author

@app.route('/authors')
def show_authors():
    author_data = Author.get_all()
    return render_template('authors.html',title='Authors',authors=author_data)

@app.route('/authors/new', methods=['POST'])
def add_author():
    data = {
        'name': request.form.get('name')
    }
    Author.add(data)
    return redirect('/authors')

@app.route('/authors/<int:author_id>')
def show_author(author_id):
    data = {
        'id': author_id
    }
    author_data = Author.get_one(data)
    return render_template('show_author.html',title='Show Author',author=author_data[0],unfavorites=author_data[1])

@app.route('/authors/<int:author_id>/favorite', methods=['POST'])
def add_author_fav(author_id):
    data = {
        'authorId': author_id,
        'bookId': request.form.get('book')
    }
    Author.favorite(data)
    return redirect(f'/authors/{author_id}')