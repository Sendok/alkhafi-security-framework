import sqlite3
import os

class LocalMemoryManager:
    """Manages short-term memory for The Garden per sender_id."""
    def __init__(self, db_path="garden_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit(); conn.close()

    def add_memory(self, sender_id: str, message: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO conversation_history (sender_id, message) VALUES (?, ?)", (sender_id, message))
        conn.commit(); conn.close()

    def get_recent_memory(self, sender_id: str, limit: int = 5) -> str:
        """Retrieves the last N messages to provide context to the LLM."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT message FROM conversation_history WHERE sender_id = ? ORDER BY timestamp DESC LIMIT ?", 
            (sender_id, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "No previous interaction."
            
        # Reverse to chronological order
        history = [row[0] for row in reversed(rows)]
        return "\n".join([f"- {msg}" for msg in history])