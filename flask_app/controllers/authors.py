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