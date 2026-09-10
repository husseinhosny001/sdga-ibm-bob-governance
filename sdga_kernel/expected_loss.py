import numpy as np

class SDGAExpectedLossEngine:
    def __init__(self):
        self.act_fail_cost = 500.0
        self.act_success_benefit = 50.0
        self.inact_fail_cost = 800.0

    def compute_decision(self, payload) -> dict:
        penalty = 0.0
        if payload.breaking_changes_detected:
            penalty += 0.25
        if payload.security_sensitive_module:
            penalty += 0.20
            
        p_success = float(np.clip(payload.confidence_score - penalty, 0.01, 0.99))
        p_fail = 1.0 - p_success
        
        l_action = (p_fail * self.act_fail_cost) - (p_success * self.act_success_benefit)
        l_inaction = 0.5 * self.inact_fail_cost
        
        if payload.security_sensitive_module and p_success < 0.60:
            decision = "CRITICAL_ABORT"
            permitted = False
        elif l_action < 0:
            decision = "EXECUTE"
            permitted = True
        else:
            decision = "HUMAN_REFERRAL"
            permitted = False
            
        return {
            "l_action": round(l_action, 2),
            "l_inaction": round(l_inaction, 2),
            "decision": decision,
            "execution_permitted": permitted
        }