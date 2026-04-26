from abc import ABC, abstractmethod
from typing import List
from al_kahfi.core.schemas import InteractionRequest, FilterResult, FinalDecision

class IFilterModule(ABC):
    """Abstract base class for all analytical skill modules (Phases 1-3)."""
    
    @abstractmethod
    def analyze(self, request: InteractionRequest) -> FilterResult:
        """
        Analyzes the incoming interaction based on the module's specific domain.
        
        Args:
            request (InteractionRequest): The incoming message and metadata.
            
        Returns:
            FilterResult: The analysis result including safety status and risk score.
        """
        pass

class IGuardrail(ABC):
    """Abstract base class for the final decision-making layer (Phase 4)."""
    
    @abstractmethod
    def evaluate(self, results: List[FilterResult]) -> FinalDecision:
        """
        Evaluates aggregated results from all modules to enforce security rules.
        
        Args:
            results (List[FilterResult]): The aggregated results from all active modules.
            
        Returns:
            FinalDecision: The absolute action to be taken.
        """
        pass