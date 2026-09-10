from pydantic import BaseModel, Field
from enum import Enum

class BobProposalPayload(BaseModel):
    proposal_id: str
    repository: str
    branch: str
    files_changed_count: int
    lines_added: int
    lines_deleted: int
    breaking_changes_detected: bool = False
    test_coverage_delta: float
    confidence_score: float
    proposed_diff_summary: str
    security_sensitive_module: bool = False

class GovernanceDecisionResponse(BaseModel):
    proposal_id: str
    decision: str
    l_action: float
    l_inaction: float
    rde_norm: float
    execution_permitted: bool
    audit_signature: str