# Author's Favorites (and not)
# Know the ID of the Author
# Method to get author by id
    # Instaniate, including a list of favorite books
# Method to get non-favorited books, passing author id
    # Get all books, join favorites
    # Set a non-favorites variable list
    # Iterate results
        # If author_id != authors.id
            # Append book instance to non-favorites list
    # Return non-favorites
from flask_app import app
from flask import redirect
from flask_app.controllers import authors
from flask_app.controllers import books

@app.route('/')
def home():
    return redirect('/authors')

if __name__=="__main__":
    app.run(debug=True)