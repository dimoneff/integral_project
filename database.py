import sqlite3


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect("inventory.db")
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.connection.rollback()
        else:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()


