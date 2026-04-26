from abc import ABC, abstractmethod
from typing import Dict, Any

class IContextProvider(ABC):
    """Abstract interface for Context and Identity Verification engines."""
    @abstractmethod
    def verify_context(self, sender_id: str, metadata: Dict[str, Any], default_country: str) -> dict:
        """
        Evaluates the metadata. 
        Returns a dictionary containing 'risk_score' (0-100) and 'reason' (str).
        """
        pass

class LocalHeuristicProvider(IContextProvider):
    """
    Advanced offline rule-based engine calculating risk based on 
    static metadata and behavioral/temporal context.
    """
    def verify_context(self, sender_id: str, metadata: Dict[str, Any], default_country: str) -> dict:
        risk_score = 0
        reasons = []

        is_new_contact = metadata.get("is_new_contact", True)
        
        # --- 1. Static Identity Checks ---
        if is_new_contact:
            risk_score += 20
            reasons.append("No prior interaction history (+20)")
        
        # If it's an enterprise/business message, is it verified?
        if metadata.get("is_business", False) and not metadata.get("is_official_account", False):
            risk_score += 30
            reasons.append("Unverified business account (+30)")

        # Spatial Anomaly
        sender_country = metadata.get("country_code", "Unknown")
        if sender_country != default_country and sender_country != "Unknown":
            risk_score += 40
            reasons.append(f"Spatial anomaly: Unexpected country code {sender_country} (+40)")

        # Entity Age
        if metadata.get("entity_age_days", 999) < 30:
            risk_score += 50
            reasons.append("Entity age is under 30 days (+50)")

        # --- 2. Behavioral & Contextual Checks (ATO Mitigation) ---
        if not is_new_contact:
            # We only evaluate behavioral anomalies for known contacts
            if metadata.get("is_abnormal_time", False):
                risk_score += 20
                reasons.append("Temporal Anomaly: Interaction outside usual hours (+20)")
            
            if metadata.get("is_new_device", False):
                risk_score += 30
                reasons.append("Device Anomaly: Unrecognized client or device (+30)")

        # --- 3. Impossible Travel (Strict Zero Trust) ---
        if metadata.get("impossible_travel_detected", False):
            risk_score += 50
            reasons.append("Contextual Anomaly: Impossible travel / IP hop detected (+50)")

        # Cap the score at 100
        risk_score = min(risk_score, 100)
        
        final_reason = " | ".join(reasons) if reasons else "Context verified: Entity behavior is normal."

        return {
            "risk_score": risk_score,
            "reason": f"Heuristics: {final_reason}"
        }

class OsintApiProvider(IContextProvider):
    """
    Connects to external Open Source Intelligence (OSINT) APIs.
    (This is a placeholder for future cloud integration like IPinfo or AbuseIPDB).
    """
    def __init__(self, ipinfo_key: str, whois_key: str):
        self.ipinfo_key = ipinfo_key
        self.whois_key = whois_key

    def verify_context(self, sender_id: str, metadata: Dict[str, Any], default_country: str) -> dict:
        # Example mock implementation for API integration
        ip_address = metadata.get("ip_address", "")
        if ip_address and (ip_address.startswith("104.") or ip_address.startswith("185.")):
            return {"risk_score": 60, "reason": "OSINT API: Known VPN/Tor IP detected (+60)"}
            
        return {"risk_score": 0, "reason": "OSINT API: Checks passed. No anomalies."}