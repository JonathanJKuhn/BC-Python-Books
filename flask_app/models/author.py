from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, db_data) -> None:
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.favorites = []

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
        unfav_query = "SELECT books.id, books.title, books.num_of_pages, books.created_at, books.updated_at, favorites.author_id FROM books LEFT JOIN favorites ON books.id = book_id;"
        unfav_res = connectToMySQL('books_schema').query_db(unfav_query)
        unfav_list = []
        for unfavorite in unfav_res:
            if unfavorite['author_id'] != data['id']:
                if len(unfav_list) == 0:
                    unfav_list.append(book.Book(unfavorite))
                else:
                    isInList = False
                    for item in unfav_list:
                        if item.id == unfavorite['id']:
                            isInList = True
                    if isInList == False:
                        unfav_list.append(book.Book(unfavorite))
                    else:
                        isInList = False
        
        return [author, unfav_list]

    @staticmethod
    def favorite(data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(authorId)s, %(bookId)s);"
        return connectToMySQL('books_schema').query_db(query, data)