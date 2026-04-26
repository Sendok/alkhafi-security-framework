from al_kahfi.core.interfaces import IFilterModule
from al_kahfi.core.schemas import InteractionRequest, FilterResult

# Import configuration
from al_kahfi.plugins.cave.config import (
    CAVE_THRESHOLD, CAVE_ENGINE_MODE, 
    LOCAL_DB_PATH, THREAT_API_URL, THREAT_API_KEY
)

# Import strategies
from al_kahfi.plugins.cave.threat_providers import (
    LocalSQLiteProvider, CloudThreatApiProvider
)

class CavePlugin(IFilterModule):
    """The Cave: Decentralized community threat intelligence layer."""
    
    def __init__(self):
        print(f"[The Cave Init] Booting Threat Intel Engine in mode: {CAVE_ENGINE_MODE}")
        
        # Strategy Factory
        if CAVE_ENGINE_MODE == "CLOUD_API":
            self.engine = CloudThreatApiProvider(api_url=THREAT_API_URL, api_key=THREAT_API_KEY)
        else:
            self.engine = LocalSQLiteProvider(db_path=LOCAL_DB_PATH)

    def analyze(self, request: InteractionRequest) -> FilterResult:
        print(f"[The Cave] Querying threat database for entity: {request.sender_id}")
        
        # Execute the chosen strategy
        analysis = self.engine.check_threat(entity_id=request.sender_id)
        
        score = analysis.get("threat_score", 0)
        reason = analysis.get("reason", "No threat data found.")
        
        is_safe = score < CAVE_THRESHOLD

        return FilterResult(
            module_name=f"The Cave ({CAVE_ENGINE_MODE})",
            is_safe=is_safe,
            score=score,
            details=reason
        )