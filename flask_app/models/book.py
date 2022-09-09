from flask_app.config.mysqlconnection import connectToMySQL

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