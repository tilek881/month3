import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    food_quality TEXT NOT NULL,
                    cleanliness INTEGER NOT NULL,
                    extra_comments TEXT
                )
            ''')
            conn.commit()

    def insert_review(self, name, contact, food_quality, cleanliness, comments):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (name, contact, food_quality, cleanliness, extra_comments)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, contact, food_quality, cleanliness, comments))
            conn.commit()

    def fetch_all_reviews(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM review')
            return cursor.fetchall()