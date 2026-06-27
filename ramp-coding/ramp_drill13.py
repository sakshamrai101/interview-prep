"""
Rules

- The Ingestion Target: You are handed a list of card transaction logs. Each has an employee_id and an amount.

- The Threshold Evaluation: * If amount is 1000.00 or higher, the category label string is "large_transaction".
  Otherwise, the category label string is "standard_transaction".

- The Guard Requirement: Start with a completely empty standard dictionary ({}). Use your single-expression .get() pattern to dynamically 
  initialize and increment the count of logs in each threshold tier.

"""

class CreditLimitAuditor:
    def __init__(self):
        # A real-time stream of incoming corporate card swiping events
        self.transaction_stream = [
            {"employee_id": "emp_1", "amount": 250.00},   # standard_transaction
            {"employee_id": "emp_2", "amount": 4500.00},  # large_transaction
            {"employee_id": "emp_3", "amount": 1000.00},  # large_transaction
            {"employee_id": "emp_4", "amount": 999.99},   # standard_transaction
            {"employee_id": "emp_5", "amount": 12500.00}, # large_transaction
        ]

    def categorize_transaction_sizes(self):

        category_size_counts = {}

        for stream in self.transaction_stream:
            if stream["amount"] >= 1000.0:
                label = "large_transaction"
            else:
                label = "standard_transaction"

            category_size_counts[label] = category_size_counts.get(label, 0.0) + 1
        
        return category_size_counts

# ---- EXECUTION HARNESS ----
if __name__ == "__main__":
    auditor = CreditLimitAuditor()
    print("---------Testing-Credit-Limit-Auditor---------")
    
    report = auditor.categorize_transaction_sizes()
    print("Final Transaction Size Tally Object:")
    print(report)
    # Expected output exactly: {'standard_transaction': 2, 'large_transaction': 3}