import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_number TEXT,
            food_rating INTEGER,
            cleanliness_rating INTEGER,
            extra_comments TEXT
        )
        ''')
        self.connection.commit()

    def save_review(self, name, phone_number, food_rating, cleanliness_rating, extra_comments):
        self.cursor.execute('''
        INSERT INTO reviews (name, phone_number, food_rating, cleanliness_rating, extra_comments)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, phone_number, food_rating, cleanliness_rating, extra_comments))
        self.connection.commit()

    def close(self):
        self.connection.close()

