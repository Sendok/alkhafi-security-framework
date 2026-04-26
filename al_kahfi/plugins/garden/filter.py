from al_kahfi.core.interfaces import IFilterModule
from al_kahfi.core.schemas import InteractionRequest, FilterResult

from al_kahfi.plugins.garden.config import (
    EMOTION_THRESHOLD, ENGINE_MODE,
    CLOUD_API_KEY, CLOUD_BASE_URL, CLOUD_MODEL_NAME,
    LOCAL_BASE_URL, LOCAL_MODEL_NAME
)
from al_kahfi.plugins.garden.prompts import SYSTEM_PROMPT
from al_kahfi.plugins.garden.cognitive_providers import (
    RegexCognitiveProvider, CloudAPIProvider, LocalOnPremProvider
)

class GardenPlugin(IFilterModule):
    """The Garden: Cognitive and emotional regulation filter layer."""
    
    def __init__(self):
        print(f"[The Garden Init] Booting Cognitive Engine in mode: {ENGINE_MODE}")
        
        # Strategy Injection: Memilih mesin berdasarkan konfigurasi
        if ENGINE_MODE == "CLOUD_API":
            self.engine = CloudAPIProvider(CLOUD_API_KEY, CLOUD_BASE_URL, CLOUD_MODEL_NAME)
        elif ENGINE_MODE == "LOCAL_ONPREM":
            self.engine = LocalOnPremProvider(LOCAL_BASE_URL, LOCAL_MODEL_NAME)
        else:
            self.engine = RegexCognitiveProvider()

    def analyze(self, request: InteractionRequest) -> FilterResult:
        print(f"[The Garden] Scanning interaction using {ENGINE_MODE} engine...")
        
        # Memanggil mesin AI / Regex untuk menganalisis teks
        analysis = self.engine.analyze_text(
            system_prompt=SYSTEM_PROMPT, 
            user_text=request.message
        )
        
        score = analysis.get("manipulation_score", 50)
        reason = analysis.get("reason", "No detailed reason provided by the engine.")
        
        is_safe = score < EMOTION_THRESHOLD

        return FilterResult(
            module_name=f"The Garden ({ENGINE_MODE})",
            is_safe=is_safe,
            score=score,
            details=f"LLM Reason: {reason}"
        )