from typing import List
from al_kahfi.core.interfaces import IFilterModule, IGuardrail
from al_kahfi.core.schemas import InteractionRequest, FinalDecision

class AlKahfiUseCase:
    """
    The agnostic core brain of the framework. 
    It routes data to independent skill modules without knowing their internal logic.
    """
    def __init__(self, filters: List[IFilterModule], guardrail: IGuardrail):
        self.filters = filters
        self.guardrail = guardrail

    def process_interaction(self, request: InteractionRequest) -> FinalDecision:
        """Executes the defense-in-depth pipeline."""
        results = []
        
        # Execute all injected filter modules (Skills) in sequence
        for filter_module in self.filters:
            res = filter_module.analyze(request)
            results.append(res)
        
        # Pass the aggregated context to the guardrails for final enforcement
        return self.guardrail.evaluate(results)