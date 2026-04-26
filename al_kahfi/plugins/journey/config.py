import os
from dotenv import load_dotenv

load_dotenv()

# Threshold for The Journey. If risk_score >= 70, entity context is unsafe.
JOURNEY_THRESHOLD = int(os.getenv("JOURNEY_THRESHOLD", "70"))

# Engine Modes: "LOCAL_HEURISTIC" (Offline rules) or "OSINT_API" (Cloud services)
JOURNEY_ENGINE_MODE = os.getenv("JOURNEY_ENGINE_MODE", "LOCAL_HEURISTIC")

# Expected default country code for spatial anomaly detection
DEFAULT_COUNTRY_CODE = os.getenv("JOURNEY_DEFAULT_COUNTRY_CODE", "+62")

# 3rd Party OSINT API Configurations (For future expansion)
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY", "")
WHOIS_API_KEY = os.getenv("WHOIS_API_KEY", "")