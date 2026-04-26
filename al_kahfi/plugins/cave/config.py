import os
from dotenv import load_dotenv

load_dotenv()

# Threshold for The Cave. If threat_score >= 80, entity is blocked.
CAVE_THRESHOLD = int(os.getenv("CAVE_THRESHOLD", "80"))

# Engine Modes: "LOCAL_DB" or "CLOUD_API"
CAVE_ENGINE_MODE = os.getenv("CAVE_ENGINE_MODE", "LOCAL_DB")

# Database Path for Local SQLite
# Defaults to a file in the current working directory for easy access
LOCAL_DB_PATH = os.getenv("CAVE_LOCAL_DB_PATH", "jamaah_threats.db")

# 3rd Party API Configurations (e.g., AbuseIPDB, VirusTotal)
THREAT_API_KEY = os.getenv("THREAT_API_KEY", "")
THREAT_API_URL = os.getenv("THREAT_API_URL", "https://api.abuseipdb.com/api/v2/check")