from fastapi import FastAPI
import hashlib, time
from wrapper_api.schemas import BobProposalPayload, GovernanceDecisionResponse
from sdga_kernel.expected_loss import SDGAExpectedLossEngine

app = FastAPI(title="SDGA v6.0 - IBM Bob Bridge")
engine = SDGAExpectedLossEngine()

@app.post("/api/v1/governance/evaluate", response_model=GovernanceDecisionResponse)
async def evaluate(payload: BobProposalPayload):
    res = engine.compute_decision(payload)
    sig = hashlib.sha256(f"{payload.proposal_id}|{res['decision']}|{time.time()}".encode()).hexdigest()
    
    return GovernanceDecisionResponse(
        proposal_id=payload.proposal_id,
        decision=res["decision"],
        l_action=res["l_action"],
        l_inaction=res["l_inaction"],
        rde_norm=0.5,
        execution_permitted=res["execution_permitted"],
        audit_signature=sig
    )

@app.get("/health")
async def health():
    return {"status": "ACTIVE"}