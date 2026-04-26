from fastapi import FastAPI, HTTPException
from al_kahfi.core.schemas import InteractionRequest, FinalDecision
from al_kahfi.core.orchestrator import AlKahfiUseCase

# Import all independent plugins (Skills & Guardrails)
from al_kahfi.plugins.garden.filter import GardenPlugin
from al_kahfi.plugins.journey.filter import JourneyPlugin
from al_kahfi.plugins.cave.filter import CavePlugin
from al_kahfi.plugins.barrier.guardrail import BarrierPlugin

# 1. Initialize the FastAPI Application
app = FastAPI(
    title="The Al-Kahfi Framework API",
    description="A Human-Centric, Zero-Trust Cybersecurity Framework for mitigating Social Engineering and Account Takeovers.",
    version="1.0.0"
)

print("========================================")
print("🛡️ Bootstrapping Al-Kahfi Framework... 🛡️")
print("========================================")

try:
    # 2. Instantiate Plugins (This will load their respective configurations)
    garden_module = GardenPlugin()
    journey_module = JourneyPlugin()
    cave_module = CavePlugin()
    barrier_module = BarrierPlugin()

    # 3. Inject dependencies into the Orchestrator (Dependency Injection)
    # Notice how the Orchestrator doesn't know the internal logic of the plugins,
    # it only relies on the IFilterModule and IGuardrail interfaces.
    orchestrator = AlKahfiUseCase(
        filters=[garden_module, journey_module, cave_module],
        guardrail=barrier_module
    )
    print("✅ All modules successfully loaded and orchestrated.\n")

except Exception as e:
    print(f"❌ Critical Error during initialization: {e}")
    raise e

# 4. Define API Endpoints
@app.post("/api/v1/scan", response_model=FinalDecision, tags=["Security Engine"])
async def scan_interaction(request: InteractionRequest):
    """
    Primary endpoint to evaluate an incoming digital interaction.
    
    The payload passes through three layers:
    1. **The Garden**: Cognitive & Emotional analysis.
    2. **The Journey**: Contextual & Identity verification (Zero Trust).
    3. **The Cave**: Community threat intelligence.
    
    Finally, **The Barrier** evaluates the results and returns an absolute decision.
    """
    try:
        # Delegate the entire process to the Use Case (Orchestrator)
        decision = orchestrator.process_interaction(request)
        return decision
    except Exception as e:
        # Catch any unexpected errors from the internal engines
        raise HTTPException(status_code=500, detail=f"Internal Engine Error: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check():
    """Simple endpoint to verify if the Al-Kahfi engine is running."""
    return {
        "status": "online",
        "message": "The Al-Kahfi Framework is active and protecting your environment."
    }