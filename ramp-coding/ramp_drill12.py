"""
Rules

- The Ingestion Target: You are handed a list of transaction dictionaries. Each has a tx_id and a float risk_score.

- The Risk Evaluation Condition: * If risk_score is 0.70 or higher, the category label is "high_risk". 
  Otherwise, the category label is "low_risk".

- The Guard Requirement: Start with a completely empty standard dictionary ({}). Use the .get() pattern to 
  dynamically initialize and increment the count of transactions in each risk tier.

"""

class RiskAssessmentEngine:
    def __init__(self):
        # A stream of fresh corporate transactions with evaluated machine learning risk scores
        self.tx_stream = [
            {"tx_id": "tx_1", "risk_score": 0.12}, # low_risk
            {"tx_id": "tx_2", "risk_score": 0.85}, # high_risk
            {"tx_id": "tx_3", "risk_score": 0.71}, # high_risk
            {"tx_id": "tx_4", "risk_score": 0.45}, # low_risk
            {"tx_id": "tx_5", "risk_score": 0.92}, # high_risk
        ]

    def categorize_transaction_risks(self):

        risk_counts = {}

        for stream in self.tx_stream:
            if stream["risk_score"] >= 0.70:
                label = "high_risk"
            else:
                label = "low_risk"
            
            risk_counts[label] = risk_counts.get(label, 0.0) + 1
        
        return risk_counts
            

# ---- EXECUTION HARNESS ----
if __name__ == "__main__":
    engine = RiskAssessmentEngine()
    print("---------Testing-Risk-Assessment-Engine---------")
    
    report = engine.categorize_transaction_risks()
    print("Final Risk Tally Object:")
    print(report)
    # Expected output exactly: {'low_risk': 2, 'high_risk': 3}