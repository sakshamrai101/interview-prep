"""
Batch Validation Engine:

Rules:

- Target Filtering: Loop through self.transaction_history. Find records where the "user" matches 
  target_user AND the "time" falls within [start_time, end_time] (inclusive).

- State Mutation: For every matching record, update its inner "status" string key from 
 "SETTLED" to "DISPUTED".

- Aggregate Math Calculation: Once the modifications are complete, run a fresh summation 
  loop to compute the exact total "amount" of money across all items in the entire database 
  whose status is currently "DISPUTED". Return that computed float sum.

"""

class FraudDisputeEngine:

    def __init__(self):
        
        self.transaction_history = [
            {"tx_id": "t1", "user": "Bob", "time": 450, "amount": 100.00, "status": "SETTLED"},
            {"tx_id": "t2", "user": "Bob", "time": 520, "amount": 250.00, "status": "SETTLED"}, # Match
            {"tx_id": "t3", "user": "Alice", "time": 550, "amount": 500.00, "status": "SETTLED"},# Wrong User
            {"tx_id": "t4", "user": "Bob", "time": 580, "amount": 120.00, "status": "SETTLED"}, # Match
            {"tx_id": "t5", "user": "Bob", "time": 650, "amount": 300.00, "status": "SETTLED"}, # Outside Window
        ]

    def execute_bulk_dispute(self, target_user, start_time, end_time):

        for record in self.transaction_history:
            if record["user"] == target_user and record["time"] >= start_time and record["time"] <= end_time:
                # update status:
                record["status"] = "DISPUTED"
        
        total_dispute_amount = 0.0

        for record in self.transaction_history:
            if record["status"] == "DISPUTED":
                total_dispute_amount += record["amount"]

        return total_dispute_amount
if __name__ == "__main__":
    disputer = FraudDisputeEngine()
    print("\n---------Testing-Batch-Dispute-Engine---------")
    
    frozen_funds = disputer.execute_bulk_dispute("Bob", 500, 600)
    print(f"Total frozen disputed funds returned by function: ${frozen_funds:.2f}")
    
    print("\n--- VERIFYING ACTUAL INNER DATABASE MUTATIONS ---")
    for tx in disputer.transaction_history:
        print(f" * Transaction: {tx['tx_id']} | User: {tx['user']} | Status Flag: {tx['status']}")
            

