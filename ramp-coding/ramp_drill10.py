"""
Rules

- The Ingestion Target: You are handed a list of transaction dictionaries. Each transaction has a department, an amount, 
  and a boolean flag is_flagged_fraud.

- The Aggregation Mapping: You must parse the stream and return a single flat dictionary showing the total sum of only 
  the fraud-flagged money per department.

- The Trap: If a department has no fraud, it should not appear in your final 
  output dictionary at all.

"""

class FraudAuditTracker:
    def __init__(self):
        # A static incoming stream of real-time card usage logs
        self.raw_stream = [
            {"dept": "Engineering", "amount": 1000.00, "is_flagged_fraud": False},
            {"dept": "Sales",       "amount": 2500.00, "is_flagged_fraud": True},  # Track
            {"dept": "Engineering", "amount": 150.00,  "is_flagged_fraud": True},  # Track
            {"dept": "Marketing",   "amount": 500.00,  "is_flagged_fraud": False},
            {"dept": "Sales",       "amount": 300.00,  "is_flagged_fraud": True},  # Track
        ]

    def aggregate_fraud_by_department(self):
        """
        YOUR TURN, BRO:
        1. Initialize a clean result dictionary: fraud_map = {}
        2. Loop through self.raw_stream.
        3. If a record has is_flagged_fraud set to True:
           - Normalize the department name string to lowercase.
           - Increment the department's running total sum inside fraud_map safely.
        4. Return the completed fraud_map.
        """
        # --- WRITE YOUR CODE HERE ---
        
        fraud_map = {}

        for stream in self.raw_stream:
            if stream["is_flagged_fraud"]:
                department = stream["dept"].lower()
                fraud_map[department] = fraud_map.get(department, 0.0) + stream["amount"]
        
        return fraud_map

# ---- EXECUTION HARNESS ----
if __name__ == "__main__":
    tracker = FraudAuditTracker()
    print("---------Testing-Fraud-Audit-Tracker---------")
    
    audit_report = tracker.aggregate_fraud_by_department()
    print("Final Fraud Summary Report Object:")
    print(audit_report)
    # Expected output: {'sales': 2800.00, 'engineering': 150.00}
    # Notice 'marketing' is completely absent because it had $0.00 fraud!