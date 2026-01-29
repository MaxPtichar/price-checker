import sqlite3

from logger_config import logger
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
        id_on_site INTEGER UNIQUE,
        items_name TEXT,
        price REAL,
        update_at DATETIME DEFAULT (datetime('now', 'localtime'))
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
        self.execute_query("INSERT OR IGNORE INTO BadId (product_id) VALUES (?)", (1,))

    def add_data(self, product: Product):
        try:
            query = """
                INSERT INTO DataFromOZ (id_on_site, items_name, price) VALUES (?,?,?)
                ON CONFLICT (id_on_site) DO UPDATE SET price = excluded.price,
                items_name = excluded.items_name,
                update_at = datetime('now', 'localtime')
            """
            params = (product.id_on_site, product.name, product.price)
            self.execute_query(query, params)
            logger.info(f"Item {product.name} successfully added")
        except Exception as e:
            logger.error(
                f"Item: {product.name},{product.id_on_site} not added. Error: {e}"
            )

    def get_all(self):
        return self.cursor.fetchall()

    def get_last_id(self) -> int:
        res = self.cursor.execute(
            'SELECT value FROM Settings WHERE key = "last_id"'
        ).fetchone()

        logger.info(f"Last ID: {res[0]}")
        return res[0] if res else 1

    def update_last_id(self, id: int):
        self.execute_query('UPDATE Settings SET value = ? WHERE key = "last_id"', (id,))

    def get_bad_id(self):
        rows = self.execute_query("SELECT product_id FROM BadId")
        return [row[0] for row in rows]

    def add_bad_id(self, prodcut_id):
        try:
            self.execute_query(
                "INSERT OR IGNORE INTO BadId (product_id) VALUES (?)", (prodcut_id,)
            )
            logger.info(f"{prodcut_id} added. ")
        except Exception as e:
            logger.error(f"{prodcut_id} not added. Error: {e}")
