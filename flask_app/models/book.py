from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, db_data) -> None:
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.favorites = []

    @staticmethod
    def add(data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books_list = []
        for result in results:
            books_list.append(cls(result))
        return books_list

    @classmethod
    def get_one(cls, data):
        book_query = "SELECT * FROM books WHERE id = %(id)s;"
        book_res = connectToMySQL('books_schema').query_db(book_query, data)
        book = cls(book_res[0])

        # Get favorites
        fav_query = "SELECT authors.id, authors.name, authors.created_at, authors.updated_at FROM books JOIN favorites ON books.id = book_id JOIN authors on authors.id = author_id WHERE books.id = %(id)s;"
        fav_res = connectToMySQL('books_schema').query_db(fav_query, data)
        for favorite in fav_res:
            book.favorites.append(author.Author(favorite))

        # Get non-favorites
        unfav_query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        unfav_res = connectToMySQL('books_schema').query_db(unfav_query, data)
        unfav_list = []
        for unfavorite in unfav_res:
            unfav_list.append(author.Author(unfavorite))

        return [book, unfav_list]

    @staticmethod
    def favorite(data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(authorId)s, %(bookId)s);"
        return connectToMySQL('books_schema').query_db(query, data)