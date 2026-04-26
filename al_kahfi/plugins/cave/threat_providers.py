import sqlite3
import os
from abc import ABC, abstractmethod

class IThreatProvider(ABC):
    """Abstract interface for Threat Intelligence providers."""
    @abstractmethod
    def check_threat(self, entity_id: str) -> dict:
        """Returns a dictionary with 'threat_score' (0-100) and 'reason' (str)."""
        pass

class LocalSQLiteProvider(IThreatProvider):
    """Queries a local SQLite database containing community-reported threats."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Creates the table and inserts dummy malicious data for testing."""
        # Ensure the directory exists if a deep path is provided
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create schema for the community blacklist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jamaah_blacklist (
                    entity_id TEXT PRIMARY KEY,
                    threat_type TEXT NOT NULL,
                    score INTEGER DEFAULT 50,
                    report_count INTEGER DEFAULT 1,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert a dummy attacker number for out-of-the-box testing
            cursor.execute('''
                INSERT OR IGNORE INTO jamaah_blacklist 
                (entity_id, threat_type, score, report_count)
                VALUES ('+6281299990000', 'phishing_scam', 95, 5)
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"[Cave DB Init Error] Failed to initialize database: {e}")
        finally:
            if conn:
                conn.close()

    def check_threat(self, entity_id: str) -> dict:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Search for the entity in the blacklist
            cursor.execute(
                "SELECT threat_type, score, report_count FROM jamaah_blacklist WHERE entity_id = ?", 
                (entity_id,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                threat_type, score, report_count = result
                reason = f"Local DB: Flagged as {threat_type} (Reported {report_count} times)."
                return {"threat_score": score, "reason": reason}
            else:
                return {"threat_score": 0, "reason": "Local DB: Entity not found in community blacklist."}
                
        except sqlite3.Error as e:
            print(f"[Cave DB Error] {e}")
            return {"threat_score": 0, "reason": f"Database Error: {str(e)}"}

class CloudThreatApiProvider(IThreatProvider):
    """
    Queries external 3rd party databases like VirusTotal or AbuseIPDB.
    (Placeholder for future expansion).
    """
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def check_threat(self, entity_id: str) -> dict:
        # Mock implementation for prototype. 
        if entity_id == "malicious_bot_01":
            return {"threat_score": 90, "reason": "Cloud API: Entity flagged by 3rd party vendor."}
            
        return {"threat_score": 0, "reason": "Cloud API: Entity is clean."}