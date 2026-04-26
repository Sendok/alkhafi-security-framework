import json
import re
import requests
from abc import ABC, abstractmethod

class ICognitiveProvider(ABC):
    """Kontrak abstrak untuk semua mesin analisis kognitif."""
    @abstractmethod
    def analyze_text(self, system_prompt: str, user_text: str) -> dict:
        pass

class RegexCognitiveProvider(ICognitiveProvider):
    """Abstract interface for all cognitive analysis engine."""
    def analyze_text(self, system_prompt: str, user_text: str) -> dict:
        text = user_text.lower()
        # Pola ancaman tingkat tinggi
        high_risk = r"\b(urgent|immediate|block|suspend|segera|blokir|hangus|transfer|password|otp)\b"
        
        if re.search(high_risk, text):
            return {
                "manipulation_score": 85, 
                "reason": "Regex Engine: High-risk urgency or credential-seeking keywords detected."
            }
            
        return {
            "manipulation_score": 10, 
            "reason": "Regex Engine: No manipulative patterns found."
        }

class CloudAPIProvider(ICognitiveProvider):
    """Connecting to API Cloud (OpenAI, Groq, etc)."""
    def __init__(self, api_key: str, base_url: str, model_name: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name

    def analyze_text(self, system_prompt: str, user_text: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "temperature": 0.0  # Suhu 0 agar output konsisten dan deterministik
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            
            raw_content = response.json()["choices"][0]["message"]["content"]
            # Pembersihan string antisipasi halusinasi format markdown LLM
            clean_json = raw_content.strip().removeprefix("```json").removesuffix("```").strip()
            
            return json.loads(clean_json)
            
        except Exception as e:
            print(f"[Cloud API Error] {str(e)}")
            return {"manipulation_score": 50, "reason": f"Cloud API timeout or parsing error."}

class LocalOnPremProvider(ICognitiveProvider):
    """Connecting to Local LLM (example: Ollama)."""
    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        self.model_name = model_name

    def analyze_text(self, system_prompt: str, user_text: str) -> dict:
        payload = {
            "model": self.model_name,
            "system": system_prompt,
            "prompt": user_text,
            "stream": False,
            "format": "json",  # Fitur Ollama untuk memaksa keluaran JSON
            "options": {"temperature": 0.0}
        }

        try:
            response = requests.post(f"{self.base_url}/generate", json=payload, timeout=30)
            response.raise_for_status()
            
            return json.loads(response.json()["response"])
            
        except Exception as e:
            print(f"[Local LLM Error] {str(e)}")
            return {"manipulation_score": 50, "reason": f"Local LLM connection failed."}