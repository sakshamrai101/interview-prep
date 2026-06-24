import time 
from collections import deque 

class MockTransactionStream:
    def __init__(self):
        # Simulated timeline of card swipes for employee "Saksham"
        # Each tuple represents: (timestamp_in_seconds, amount_spent)
        # We have the stream array as 
        self.stream = [
            (1719176400, 150.00),  # T = 0 seconds: First purchase
            (1719176430, 200.00),  # T = 30 seconds: 30 seconds later
            (1719176520, 500.00),  # T = 120 seconds: 2 minutes after start
            (1719176710, 100.00),  # T = 310 seconds: 5 minutes + 10 seconds after start
            (1719176720, 2000.00)  # T = 320 seconds: High velocity threat check!
        ]

card_stream = MockTransactionStream().stream

class RampVelocityEngine: 
    def __init__(self, window_seconds=300):
        # 1. Config: How far back do we look? (300 seconds = 5 minutes)
        self.window_seconds = window_seconds
        
        # 2. State Tracker: A deque of tuples holding our active history: (timestamp, amount)
        self.active_transactions = deque()

        # 3. Running sum tracker wihtin the active window 
        self.current_window_sum = 0.0
    
    def add_transaction_and_check_risk(self, timestamp, amount):
        """
        RISK SLIDER:
        Add a new transaction, purges old expired entries out of the deque,
        updates the running window sum, and flags a warning if the total breaches $1,500.00

        """
        # STEP A: Append the brand new transaction to our history loop
        self.active_transactions.append((timestamp, amount))
        self.current_window_sum += amount

        # STEP B: The Cleanup. We look at the oldest item on the left.
        # If its timestamp is older than (current_timestamp - window_seconds),
        # it has fallen out of our window! We must pop it off and subtract its amount.

        # while deque not empty 
        while self.active_transactions and self.active_transactions[0][0] < (timestamp - self.window_seconds):
            old_timestamp, old_amount = self.active_transactions.popleft()
            self.current_window_sum -= old_amount
        
        print(f"[ENGINE] Added ${amount:.2}. Current Window Todal: ${self.current_window_sum:.2f}")

        # Rule Check: If total volume in the last 5 mins breaches $1500.00, return True (Risk Flagged)
        if self.current_window_sum > 1500.00:
            return True 
        
        return False 


if __name__ == "__main__":
    engine = RampVelocityEngine(window_seconds=300) # 5 minute window 
    print("--- STARTING HIGH-FREQUENCY VELOCITY RUN ---")

    for ts, amt in card_stream:
        print(f"\n👉 New Swipe Event! Timestamp: {ts} | Amount: ${amt:.2f}")
        is_fraud_risk = engine.add_transaction_and_check_risk(ts, amt)
        if is_fraud_risk:
            print(" [ALERT] RISK TRIGGERED! CARD LOOKED FOR SUSPICIOUS VELOCITY.")
        else:
            print("Approved, safe transaction velocity")
    



