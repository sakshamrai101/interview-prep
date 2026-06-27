"""
Rules 

- The Multiplier Matrix: Ramp awards different cashback points based on the transaction type: 
  "software" ➔ Earns 4x points per dollar spent
  "marketing" ➔ Earns 2x points per dollar spent
  Any other category ➔ Earns a baseline 1x point per dollar spent

 - The Guard Requirement: Start with a completely empty standard dictionary ({}). For each transaction, multiply the amount by its corresponding modifier and accumulate the total points earned per category dynamically using the .get() pattern.
"""

class CashbackEngine:
    def __init__(self):
        self.transaction_history = [
            {"category": "software",  "amount": 100.00}, # 100 * 4 = 400 points
            {"category": "marketing", "amount": 200.00}, # 200 * 2 = 400 points
            {"category": "software",  "amount": 50.00},  # 50 * 4  = 200 points
            {"category": "dining",    "amount": 50.00},  # 50 * 1  = 50 points (Other)
        ]

    def calculate_points_pool(self):

        category_points_aggregrator = {}

        for transaction in self.transaction_history:
            if transaction["category"] == "software":
                multiplier = 4
            elif transaction["category"] == "marketing":
                multiplier = 2
            else:
                multiplier = 1
            
            category_points_aggregrator[transaction["category"]] = category_points_aggregrator.get(transaction["category"], 0.0) + transaction["amount"] * multiplier
        
        return category_points_aggregrator

    
if __name__ == "__main__":
    engine = CashbackEngine()
    print("---------Testing-Cashback-Engine---------")
    
    report = engine.calculate_points_pool()
    print("Final Cashback Points Tally:")
    print(report)
    
    # Assertions to verify the math logic matches requirements perfectly
    assert report.get("software") == 600.00, f"Expected 600.00 points for software, got {report.get('software')}"
    assert report.get("marketing") == 400.00, f"Expected 400.00 points for marketing, got {report.get('marketing')}"
    assert report.get("dining") == 50.00, f"Expected 50.00 points for dining, got {report.get('dining')}"
    print("\n✅ [PASSED] Tiered cashback math and dynamic accumulations are 100% accurate!")