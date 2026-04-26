from pydantic import BaseModel, Field
from typing import Dict, Any, List
from enum import Enum

# Standardized Enums for predictable Frontend handling
class ActionType(str, Enum):
    ALLOW = "ALLOW"
    ISOLATE = "ISOLATE"
    FORCE_OOB_AUTH = "FORCE_OOB_AUTH"
    BLOCK = "BLOCK"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class InteractionRequest(BaseModel):
    """Schema representing an incoming digital interaction."""
    
    message: str = Field(..., description="The text content of the message")
    sender_id: str = Field(..., description="Unique identifier of the sender")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("message")
    @classmethod
    def sanitize_newlines(cls, v: str) -> str:
        return v.strip().replace("\r\n", "\\n").replace("\n", "\\n")
        
class FilterResult(BaseModel):
    """Schema representing the output of a single filter module."""
    module_name: str
    is_safe: bool
    score: int = Field(..., ge=0, le=100, description="Risk/Safety score. Higher score generally means higher risk.")
    details: str

class FinalDecision(BaseModel):
    """Refined schema for the final frontend-ready response."""
    action: ActionType
    risk_level: RiskLevel
    overall_score: int = Field(..., description="Aggregated risk score (usually the maximum of all layers)")
    system_reason: str = Field(..., description="Detailed technical reason for backend logging")
    user_message: str = Field(..., description="Clean, localized message to display to the end-user")
    filter_logs: List[FilterResult] = Field(..., description="Audit trail of all filter layers")