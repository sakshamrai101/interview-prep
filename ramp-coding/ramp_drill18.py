class RefundLedgerReflector:
    def __init__(self):
        self.event_stream = [
            {"category": "software",  "amount": 500.00, "type": "CHARGE"}, # software starts at +500
            {"category": "travel",    "amount": 200.00, "type": "CHARGE"}, # travel starts at +200
            {"category": "software",  "amount": 100.00, "type": "REFUND"}, # software drops to +400
            {"category": "travel",    "amount": 50.00,  "type": "CHARGE"}, # travel rises to +250
            {"category": "software",  "amount": 50.00,  "type": "REFUND"}, # software drops to +350
        ]

    def calculate_net_spend(self):

        net_spend = {}

        for stream in self.event_stream:
            if stream["type"] == "CHARGE":
                net_spend[stream["category"]] = net_spend.get(stream["category"], 0.0) + stream["amount"]
            else:
                net_spend[stream["category"]] = net_spend.get(stream["category"], 0.0) - stream["amount"]
        
        return net_spend
        """
        YOUR TURN, BRO:
        1. Initialize an empty standard dict: net_spend = {}
        2. Loop through self.event_stream.
        3. Evaluate if type is "CHARGE" or "REFUND" to determine if you add or subtract the amount.
        4. Use the .get() pattern to update net_spend[category] safely.
        5. Return net_spend.
        """
        # --- WRITE YOUR CODE HERE ---
        pass

# ---- THE TEST HARNESS ----
if __name__ == "__main__":
    reflector = RefundLedgerReflector()
    print("---------Testing-Refund-Ledger-Reflector---------")
    
    report = reflector.calculate_net_spend()
    print("Final Net Spend Tally Object:")
    print(report)
    
    # Assertions to verify your loops and math match the spec perfectly
    assert report.get("software") == 350.00, f"Expected 350.00 for software, got {report.get('software')}"
    assert report.get("travel") == 250.00, f"Expected 250.00 for travel, got {report.get('travel')}"
    print("\n✅ [PASSED] Refund tracking and dynamic math adjustments are 100% accurate!")