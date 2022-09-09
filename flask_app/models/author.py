from flask_app.config.mysqlconnection import connectToMySQL

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