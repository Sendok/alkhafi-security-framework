from al_kahfi.core.interfaces import IGuardrail
from al_kahfi.core.schemas import FilterResult, FinalDecision, ActionType, RiskLevel
from typing import List

class BarrierPlugin(IGuardrail):
    """
    The Barrier: Absolute infrastructure defense and rule enforcement.
    Outputs clean, frontend-ready API responses with English localization.
    """
    
    def evaluate(self, results: List[FilterResult]) -> FinalDecision:
        # Default Safe State
        action = ActionType.ALLOW
        risk_level = RiskLevel.LOW
        system_reason = "All layers report safe and consistent interaction."
        user_message = "Safe: This message comes from a verified and trusted source."
        
        # Calculate overall score (using the highest risk score detected across all layers)
        overall_score = max([res.score for res in results]) if results else 0

        # Extract specific module results for cross-validation
        garden_res = next((r for r in results if "The Garden" in r.module_name), None)
        journey_res = next((r for r in results if "The Journey" in r.module_name), None)
        cave_res = next((r for r in results if "The Cave" in r.module_name), None)

        # ---------------------------------------------------------
        # RULE 1: CRITICAL THREAT (Community Blacklist)
        # ---------------------------------------------------------
        # If the sender is already marked as a threat by the community, block immediately.
        if cave_res and not cave_res.is_safe:
            return FinalDecision(
                action=ActionType.BLOCK,
                risk_level=RiskLevel.CRITICAL,
                overall_score=overall_score,
                system_reason="Critical: Entity exists in community threat database.",
                user_message="⚠️ BLOCKED: This sender is on the community blacklist (High risk of Scam/Spam).",
                filter_logs=results
            )

        # ---------------------------------------------------------
        # RULE 2: ACCOUNT TAKEOVER MITIGATION (The Mismatch Trigger)
        # ---------------------------------------------------------
        # If the context is safe (e.g., trusted contact, no IP anomaly) 
        # BUT the emotion is highly manipulative, it indicates a hijacked account.
        if garden_res and journey_res:
            if not garden_res.is_safe and journey_res.is_safe:
                return FinalDecision(
                    action=ActionType.FORCE_OOB_AUTH,
                    risk_level=RiskLevel.HIGH,
                    overall_score=overall_score,
                    system_reason="Critical Mismatch: Trusted contact using high-risk emotional manipulation. Potential ATO.",
                    user_message="🛑 WARNING: Your trusted contact is requesting urgent action. Please make a voice or video call to verify their identity before proceeding, as their account may be compromised.",
                    filter_logs=results
                )

        # ---------------------------------------------------------
        # RULE 3: ISOLATION (High Anomaly / Manipulation)
        # ---------------------------------------------------------
        # If any layer breaches the safety threshold without triggering the above rules.
        if overall_score >= 70:
            return FinalDecision(
                action=ActionType.ISOLATE,
                risk_level=RiskLevel.MEDIUM,
                overall_score=overall_score,
                system_reason="Warning: High anomaly or emotional manipulation detected. Routing to Sandbox.",
                user_message="🟡 CAUTION: This message contains suspicious urgency or anomalies. The interaction has been isolated for your safety.",
                filter_logs=results
            )

        # ---------------------------------------------------------
        # DEFAULT: SAFE
        # ---------------------------------------------------------
        return FinalDecision(
            action=action,
            risk_level=risk_level,
            overall_score=overall_score,
            system_reason=system_reason,
            user_message=user_message,
            filter_logs=results
        )