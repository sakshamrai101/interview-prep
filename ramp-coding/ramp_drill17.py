"""

Rules 

- The Liquidity Pool: A company sets a master cash balance pool. Every time an employee swipes their card, 
  you must deduct that amount from the company's remaining cash balance.

- The Hard Stop Guard: If an individual transaction amount is greater than the remaining cash balance, the transaction must be rejected, and you must increment a "declined_swipes" counter. 
  If it clears, deduct the cash and increment an "approved_swipes" counter.

- The Guard Requirement: Start with a completely empty standard dictionary ({}). 
  Use the .get() pattern on a single line to update your transaction counters safely.

"""

class OverdraftSafeguard:
    def __init__(self):
        self.company_cash_pool = 500.00  # Starting cash balance
        self.swipe_stream = [
            {"tx_id": "s1", "amount": 150.00}, # Approved (Pool drops to 350)
            {"tx_id": "s2", "amount": 400.00}, # Declined (400 > 350! Pool stays 350)
            {"tx_id": "s3", "amount": 200.00}, # Approved (Pool drops to 150)
            {"tx_id": "s4", "amount": 50.00},  # Approved (Pool drops to 100)
            {"tx_id": "s5", "amount": 150.00}, # Declined (150 > 100! Pool stays 100)
        ]
    

    def process_swipes(self):

        swipe_status_counter = {}

        for stream in self.swipe_stream:
            deficit = self.company_cash_pool - stream["amount"]

            if deficit > 0:
                label = "approved_swipes"
                self.company_cash_pool -= stream["amount"]
                swipe_status_counter[label] = swipe_status_counter.get(label, 0.0) + 1
            else:
                label = "declined_swipes"
                swipe_status_counter[label] = swipe_status_counter.get(label, 0.0) + 1
        
        return swipe_status_counter

if __name__ == "__main__":
    safeguard = OverdraftSafeguard()
    print("---------Testing-Overdraft-Safeguard---------")
    
    # 1. Capture the initial state of the cash pool
    initial_pool = safeguard.company_cash_pool
    
    # 2. Run the processing stream
    report = safeguard.process_swipes()
    print("Final Transaction Processing Tally:")
    print(report)
    print(f"Remaining Cash Pool Balance: ${safeguard.company_cash_pool:.2f}")
    
    # Assertions to verify the counter math matches requirements perfectly
    assert report.get("approved_swipes") == 3, f"Expected 3 approved swipes, got {report.get('approved_swipes')}"
    assert report.get("declined_swipes") == 2, f"Expected 2 declined swipes, got {report.get('declined_swipes')}"
    
    # Assertion to verify correct mutations on the parent tracking variable
    # $500.00 - $150.00 (s1) - $200.00 (s3) - $50.00 (s4) = $100.00
    assert safeguard.company_cash_pool == 100.00, f"Expected cash pool to be 100.00, got {safeguard.company_cash_pool}"
    
    print("\n✅ [PASSED] Overdraft restrictions, state updates, and tracking counters are 100% accurate!")