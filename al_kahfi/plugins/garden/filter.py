import os
from al_kahfi.core.interfaces import IFilterModule
from al_kahfi.core.schemas import InteractionRequest, FilterResult
from al_kahfi.plugins.garden.config import ENGINE_MODE, EMOTION_THRESHOLD
from al_kahfi.plugins.garden.cognitive_providers import RegexCognitiveProvider, CloudAPIProvider, LocalOnPremProvider
from al_kahfi.plugins.garden.memory import LocalMemoryManager

class GardenPlugin(IFilterModule):
    def __init__(self):
        # 1. Load The Soul (System Prompt)
        self.soul_path = os.getenv("GARDEN_SOUL_PATH", "soul.md")
        self.system_prompt = self._load_soul()
        
        # 2. Initialize Memory
        self.memory = LocalMemoryManager()

        # 3. Initialize Engine
        if ENGINE_MODE == "CLOUD_API":
            self.engine = CloudAPIProvider(...) # (parameter seperti sebelumnya)
        elif ENGINE_MODE == "LOCAL_ONPREM":
            self.engine = LocalOnPremProvider(...)
        else:
            self.engine = RegexCognitiveProvider()

    def _load_soul(self) -> str:
        """Reads the soul/prompt from an external file."""
        if os.path.exists(self.soul_path):
            with open(self.soul_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Evaluate the message for manipulation (0-100). Respond ONLY in JSON."

    def analyze(self, request: InteractionRequest) -> FilterResult:
        # A. Ambil ingatan masa lalu
        past_context = self.memory.get_recent_memory(request.sender_id)
        
        # B. Gabungkan pesan baru dengan ingatan masa lalu agar LLM paham konteks
        contextualized_prompt = f"Previous Context:\n{past_context}\n\nNew Message to Evaluate:\n{request.message}"
        
        # C. Evaluasi menggunakan The Soul + Contextual Prompt
        analysis = self.engine.analyze_text(self.system_prompt, contextualized_prompt)
        
        # D. Simpan pesan baru ke memori untuk interaksi berikutnya
        self.memory.add_memory(request.sender_id, request.message)

        score = analysis.get("manipulation_score", 50)
        return FilterResult(
            module_name=f"The Garden ({ENGINE_MODE})", 
            is_safe=score < EMOTION_THRESHOLD, 
            score=score, 
            details=analysis.get("reason", "No reason.")
        )