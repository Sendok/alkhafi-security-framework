import os
from dotenv import load_dotenv

load_dotenv()

# Ambang batas emosi. Jika skor >= 75, pesan dianggap berbahaya.
EMOTION_THRESHOLD = 75

# Mode Mesin: "REGEX", "CLOUD_API", atau "LOCAL_ONPREM"
ENGINE_MODE = os.getenv("GARDEN_ENGINE_MODE", "REGEX")

# Konfigurasi Cloud API (OpenAI, Groq, Claude)
CLOUD_API_KEY = os.getenv("GARDEN_CLOUD_API_KEY", "")
CLOUD_BASE_URL = os.getenv("GARDEN_CLOUD_BASE_URL", "https://api.openai.com/v1")
CLOUD_MODEL_NAME = os.getenv("GARDEN_CLOUD_MODEL", "gpt-3.5-turbo")

# Konfigurasi Local / On-Premise (Ollama, LM Studio)
LOCAL_BASE_URL = os.getenv("GARDEN_LOCAL_BASE_URL", "http://localhost:11434/api")
LOCAL_MODEL_NAME = os.getenv("GARDEN_LOCAL_MODEL", "llama3")