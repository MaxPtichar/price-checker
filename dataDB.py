import sqlite3
from os import name

from model import Product


class Database:
    def __init__(self, name_db) -> None:

        self.connection = sqlite3.connect(name_db)
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS DataFromOZ(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        items_name TEXT UNIQUE,
        price INTEGER
        );"""
        self.execute_query(query)

    def add_data(self, product: Product):
        query = (
            "INSERT INTO DataFromOZ (items_name, price) VALUES (?,?)"
            "ON CONFLICT (items_name) DO UPDATE SET price = excluded.price"
        )
        params = (product.name, product.price)
        self.execute_query(query, params)

    def get_all(self):
        return self.cursor.fetchall()
