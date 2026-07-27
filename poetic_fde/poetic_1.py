"""
Poetic automates enterprise Standard Operating Procedures (SOPs). 
A client needs a light evaluation engine to process incoming financial dispute requests and 
determine whether a dispute can be automatically approved, flagged for manual review, or rejected.

"""


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

        """

        input format: 

        {
        "dispute_id": 123,
        "amount": 100,
        "dispute_days_old": 15,
        "account_tier": "STANDARD",
        "merchant_category": 
        "status": "ACTIVE"
        }

        output format: 
        {
        "dispute_id": 123,
        "decision": "APPROVED",
        "reasons": ["Auto-approved: VIP tier amount within threshold."]
        } 
        """

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



        



