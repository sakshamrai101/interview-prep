"""

part 1 
Poetic automates enterprise Standard Operating Procedures (SOPs). 
A client needs a light evaluation engine to process incoming financial dispute requests and 
determine whether a dispute can be automatically approved, flagged for manual review, or rejected.



class DisputeEngine:

    def __init__(self, transaction):
        self.transaction = transaction
        self.valid_duration = 90
        self.approved_amount_standard = 50.00
        self.approved_amount_vip = 200.00
        self.transaction_category = set(["GROCERY", "RIDE-SHARE"])
    
    def process_disputes(self):
        return self.evaluate_dispute(self.transaction)

    
    def evaluate_dispute(self, dispute: dict) -> dict:

        if not dispute:
            return {
                "dispute_id": None,
                "decision": None,
                "reasons": None
            }
        dispute_id = dispute["dispute_id"]
        dispute_amount = dispute["amount"]
        
        # To return actual response 
        result = {"dispute_id": "", "decision": "", "reasons": ""}
        
        # Reject Condition:
        if dispute["dispute_days_old"] > self.valid_duration or dispute["status"] == "SUSPENDED":
            # Reason Condition:
            if dispute["dispute_days_old"] > self.valid_duration:
                result = {"dispute_id": dispute_id, "decision": "REJECTED", "reason": [f"Auto-Rejected: Dispute claim for dispute_id: {dispute_id} is rejected because it's older than 90 days."]}
                return result
            elif dispute["status"] == 'SUSPENDED':
                result = {"dispute_id": dispute["dispute_id"], "decision": "REJECTED", "reason": [f"Auto-Rejected: Dispute claim for dispute_id: {dispute_id} is rejected because acount is suspended."]}
                return result
        elif dispute["amount"] <= self.approved_amount_standard and dispute["merchant_category"] in self.transaction_category:
            result = {"dispute_id": dispute_id, "decision": "APPROVED", "reason": [f"Auto-Approved: Dispute claim for dispute_id: {dispute_id} is approved because dispute amount: {dispute_amount} is under valid dispute amount limit (standard) and dispute category is under {self.transaction_category}"]}
            return result
        elif dispute["account_tier"] == "VIP" and dispute_amount <= self.approved_amount_vip:
            result = {"dispute_id": dispute_id, "decision": "APPROVED", "reason": [f"Auto-Approved: Dispute claim for dispute_id: {dispute_id} is approved because dispute amount: {dispute_amount} is under valid dispute amount limit (vip) and dispute account tier is VIP."]}
            return result
        else:
            result = {"dispute_id": dispute_id, "decision": "MANUAL REVIEW", "reason": [f"MANUAL REVIEW: Dispute claim for dispute_id: {dispute_id} is put for Manual Review as it does not meet conditions of auto review and auto reject."]}
            return result

if __name__ == "__main__":
    d2 = {
        "dispute_id": "DSP-002",
        "amount": 150.00,
        "dispute_days_old": 100,
        "merchant_category": "ELECTRONICS",
        "account_tier": "VIP",
        "status": "ACTIVE"
        }

    engine = DisputeEngine(d2)
    print(engine.process_disputes())


"""

"""
part 2: 

# The client passes their custom rules configuration to the engine
rules_config = [
    {"id": "R1", "field": "dispute_days_old", "op": ">", "value": 90, "risk_score": 50, "action": "REJECT"},
    {"id": "R2", "field": "status", "op": "==", "value": "SUSPENDED", "risk_score": 100, "action": "REJECT"},
    {"id": "R3", "field": "amount", "op": ">", "value": 1000.00, "risk_score": 30, "action": "FLAG"},
]

expected output:

{
    "dispute_id": "DSP-101",
    "decision": "REJECTED",        # Because R1 triggered a "REJECT" action
    "total_risk_score": 80,        # 50 (from R1) + 30 (from R3)
    "triggered_rule_ids": ["R1", "R3"]
}
"""



"""

-> class DisputeEngine that will initialise rules config 
-> member fns to take dispute object and check from rules config to flag 
-> in main, we will create DisputeEngine obj and call member fn to evaluate a sample dispute 
"""

class DisputeEngine:

    def __init__(self, rules):
        # loads up rules config on engine instance 
        self.rules = rules
    
    def process_disputes(self, dispute_transaction: dict) -> dict:
        return self.evaluate_dispute(dispute_transaction)
    
    # helper to evaluate dynamic string comparison operator 
    def evaluate_operator(self, val1, op, val2) -> bool:
        if val1 is None:
            return False 
        
        if op == ">": return val1 > val2
        if op == "<": return val1 < val2
        if op == "==": return val1 == val2
        if op == ">=": return val1 >= val2
        if op == "<=": return val1 <= val2
        if op == "in": return val1 in val2
        return False

    
    def evaluate_dispute(self, dispute: dict) -> dict:
        # variables to build final result object
        total_risk_score = 0
        has_rejection = False
        triggered_rule_ids = []

        # check dispute against every rule 
        for rule in self.rules:
            field_name = rule["field"]
            operator = rule["op"]
            target_value = rule["value"]

            dispute_value = dispute.get(field_name)

            # check if condition matches 
            if self.evaluate_operator(dispute_value, operator, target_value):
                total_risk_score += rule.get("risk_score", 0)
                triggered_rule_ids.append(rule["id"])

                if rule.get("action") == "REJECT":
                    has_rejection = False 
            
            # final decision based on aggregated outcomes:
            if has_rejection:
                decision = "REJECTED"
            elif total_risk_score >= 50:
                decision = "MANUAL REVIEW"
            else:
                decision = "APPROVED"
            
            return {
                "dispute_id": dispute.get("dispute_id"),
                "decision": decision,
                "total_risk_score": total_risk_score,
                "triggered_rule_ids": triggered_rule_ids
            }


if __name__ == "__main__":

    dispute_1 = {
        "dispute_id": "DSP-101",
        "amount": 1200.00,
        "dispute_days_old": 95,
        "status": "ACTIVE"
    }
    rules_config = [
        {"id": "R1", "field": "dispute_days_old", "op": ">", "value": 90, "risk_score": 50, "action": "REJECT"},
        {"id": "R2", "field": "status", "op": "==", "value": "SUSPENDED", "risk_score": 100, "action": "REJECT"},
        {"id": "R3", "field": "amount", "op": ">", "value": 1000.00, "risk_score": 30, "action": "FLAG"},
    ]
    engine = DisputeEngine(rules=rules_config)
    print(engine.process_disputes(dispute_1))