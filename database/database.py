import sqlite3
from utils.logger import logger


class DatabaseClient:
    """Třída pro interakci s SQLite databází."""

    def __init__(self, db_path='articles.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        """Vytvoření tabulky articles pokud ještě neexistuje."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    topic TEXT UNIQUE
                )
            ''')

    def topic_exists(self, topic):
        """Zkontroluje, zda téma již existuje v databázi."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM articles WHERE topic = ?', (topic,))
        return cursor.fetchone() is not None

    def save_topic(self, topic):
        """Uloží nové téma do databáze."""
        with self.conn:
            self.conn.execute(
                'INSERT INTO articles (topic) VALUES (?)', (topic,))
            logger.debug(f"Téma '{topic}' bylo uloženo do databáze.")
