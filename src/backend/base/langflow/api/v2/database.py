import sqlite3
from datetime import datetime
from pathlib import Path

class ChatDatabase:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                assistant_message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_message(self, user_message: str, assistant_message: str):
        """Save a message exchange to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (user_message, assistant_message)
            VALUES (?, ?)
        ''', (user_message, assistant_message))
        
        conn.commit()
        conn.close()

    def get_chat_history(self, limit: int = 50):
        """Retrieve chat history from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_message, assistant_message, timestamp
            FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        messages = cursor.fetchall()
        conn.close()
        
        return messages 