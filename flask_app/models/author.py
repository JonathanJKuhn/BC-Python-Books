from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, db_data) -> None:
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.favorites = []

    def __repr__(self):
        return (
            f'id: {self.id}\n'
            f'name: {self.name}\n'
            f'created_at: {self.created_at}\n'
            f'updated_at: {self.updated_at}\n'
        )

    @staticmethod
    def add(data):
       query = "INSERT INTO authors (name) VALUES (%(name)s);"
       return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books_schema').query_db(query)
        authors_list = []
        for result in results:
            authors_list.append(cls(result))
        return authors_list
    
    @classmethod
    def get_one(cls, data):
        author_query = "SELECT * FROM authors WHERE id = %(id)s;"
        author_res = connectToMySQL('books_schema').query_db(author_query, data)
        author = cls(author_res[0])

        # Get favorites
        fav_query = "SELECT books.id, books.title, books.num_of_pages, books.created_at, books.updated_at FROM authors JOIN favorites ON authors.id = author_id JOIN books on books.id = book_id WHERE authors.id = %(id)s;"
        fav_res = connectToMySQL('books_schema').query_db(fav_query, data)
        for favorite in fav_res:
            author.favorites.append(book.Book(favorite))

        # Get non-favorites
        unfav_query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        unfav_res = connectToMySQL('books_schema').query_db(unfav_query, data)
        unfav_list = []
        for unfavorite in unfav_res:
            unfav_list.append(book.Book(unfavorite))    
        
        return [author, unfav_list]

    @staticmethod
    def favorite(data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(authorId)s, %(bookId)s);"
        return connectToMySQL('books_schema').query_db(query, data)