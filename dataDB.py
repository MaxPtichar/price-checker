import sqlite3

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
        self.execute_query(
            """CREATE TABLE IF NOT EXISTS DataFromOZ(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        items_name TEXT UNIQUE,
        price INTEGER
        );"""
        )

        self.execute_query(
            """CREATE TABLE IF NOT EXISTS BadId(
                            product_id INTEGER PRIMARY KEY);"""
        )

        self.execute_query(
            """CREATE TABLE IF NOT EXISTS Settings(
                            key TEXT PRIMARY KEY,
                           value INTEGER);"""
        )

        self.execute_query(
            "INSERT OR IGNORE INTO Settings (key, value) VALUES (?, ?)",
            ("last_id", 101436802),
        )

    def add_data(self, product: Product):
        query = (
            "INSERT INTO DataFromOZ (items_name, price) VALUES (?,?)"
            "ON CONFLICT (items_name) DO UPDATE SET price = excluded.price"
        )
        params = (product.name, product.price)
        self.execute_query(query, params)

    def get_all(self):
        return self.cursor.fetchall()

    def get_last_id(self) -> int:
        res = self.cursor.execute('SELECT value FROM Settings WHERE key = "last_id"')
        return res[0][0] if res else 0

    def update_last_id(self, id: int):
        self.execute_query('UPDATE Setiings SET value = ? WHERE key = "last_id"', (id,))

    def get_bad_id(self):
        rows = self.execute_query("SELECT product_id FROM BadId")
        return [row[0] for row in rows]

    def add_bad_id(self, prodcut_id):
        self.execute_query(
            "INSERT OR IGNORE INTO BadId (product_id) VALUES (?)", (prodcut_id,)
        )
