from al_kahfi.core.interfaces import IFilterModule
from al_kahfi.core.schemas import InteractionRequest, FilterResult

# Import configuration
from al_kahfi.plugins.journey.config import (
    JOURNEY_THRESHOLD, JOURNEY_ENGINE_MODE, DEFAULT_COUNTRY_CODE,
    IPINFO_API_KEY, WHOIS_API_KEY
)

# Import strategies
from al_kahfi.plugins.journey.context_providers import (
    LocalHeuristicProvider, OsintApiProvider
)

class JourneyPlugin(IFilterModule):
    """The Journey: Contextual and identity validation (Zero Trust layer)."""
    
    def __init__(self):
        print(f"[The Journey Init] Booting Context Engine in mode: {JOURNEY_ENGINE_MODE}")
        
        # Strategy Factory
        if JOURNEY_ENGINE_MODE == "OSINT_API":
            self.engine = OsintApiProvider(ipinfo_key=IPINFO_API_KEY, whois_key=WHOIS_API_KEY)
        else:
            self.engine = LocalHeuristicProvider()

    def analyze(self, request: InteractionRequest) -> FilterResult:
        print(f"[The Journey] Validating metadata for sender: {request.sender_id}")
        
        # Execute the chosen strategy
        analysis = self.engine.verify_context(
            sender_id=request.sender_id,
            metadata=request.metadata,
            default_country=DEFAULT_COUNTRY_CODE
        )
        
        score = analysis.get("risk_score", 0)
        reason = analysis.get("reason", "No anomalies detected.")
        
        # Validate against the configured threshold
        is_safe = score < JOURNEY_THRESHOLD

        return FilterResult(
            module_name=f"The Journey ({JOURNEY_ENGINE_MODE})",
            is_safe=is_safe,
            score=score,
            details=reason
        )