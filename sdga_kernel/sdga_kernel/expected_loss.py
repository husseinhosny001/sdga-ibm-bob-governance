import numpy as np
from typing import Dict, Any, Tuple

class SDGAExpectedLossEngine:
    """
    SDGA v6.0 Sovereign Kernel
    Calculates Expected Loss over Action vs Inaction using FHRR-bounded parameters.
    """
    def __init__(self, cost_matrix: Dict[str, float] = None):
        self.cost_matrix = cost_matrix or {
            "act_fail_cost": 500.0,
            "act_success_benefit": 50.0,
            "inact_fail_cost": 800.0
        }
        self.d_dimension = 10000

    def compute_decision(self, payload: Any) -> Dict[str, Any]:
        # 1. Calculate risk penalties based on change parameters
        penalty = 0.0
        if payload.breaking_changes_detected:
            penalty += 0.25
        if payload.security_sensitive_module:
            penalty += 0.20
        if payload.test_coverage_delta < 0:
            penalty += abs(payload.test_coverage_delta) * 0.30

        # 2. Risk-adjusted success probability
        p_success = float(np.clip(payload.confidence_score - penalty, 0.01, 0.99))
        p_fail = 1.0 - p_success

        # 3. Dynamic scaling factor for sensitive components
        gamma_dyn = 0.20 if payload.security_sensitive_module else 1.00

        # 4. Expected Loss Equations (L_action vs L_inaction)
        l_action = (p_fail * self.cost_matrix["act_fail_cost"]) - \
                   (p_success * self.cost_matrix["act_success_benefit"] * gamma_dyn)

        p_inaction_risk = 0.60 if payload.security_sensitive_module else 0.30
        l_inaction = p_inaction_risk * self.cost_matrix["inact_fail_cost"]

        # 5. Normalized Decision Index (RDE_norm)
        delta_l = l_inaction - l_action
        norm_factor = max(abs(l_action), abs(l_inaction), 1.0)
        rde_norm = float(np.clip(delta_l / norm_factor, -1.0, 1.0))

        # 6. Strict Decision Gates
        if payload.security_sensitive_module and p_success < 0.60:
            decision = "CRITICAL_ABORT"
            permitted = False
        elif l_action < 0 and rde_norm > 0.30:
            decision = "EXECUTE"
            permitted = True
        elif l_inaction > l_action:
            decision = "HUMAN_REFERRAL"
            permitted = False
        else:
            decision = "SAFE_ABORT"
            permitted = False

        return {
            "l_action": round(l_action, 4),
            "l_inaction": round(l_inaction, 4),
            "rde_norm": round(rde_norm, 4),
            "gamma_dynamic": gamma_dyn,
            "decision": decision,
            "execution_permitted": permitted
        }