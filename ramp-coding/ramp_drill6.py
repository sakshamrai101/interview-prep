"""
Business Requirements:

- Employees can spend as much on 'Software'
- Max Total = 5000$ across entire company on 'Travel per month'
- Input: stream of transactions 
- What to do ?

    - if any transaction pushes any category over allowed budget cap -> DENIED, don't add to category total
    - if APRROVED, add to category sum

"""

class RampSpendCapEngine:

    def __init__(self):

        # categories and their caps:
        self.category_caps = {
            "travel": 5000.00,
            "software": 10000.00,
            "marketing": 15000.00
        }

        # dict to track current spend per category: "category" -> amt
        self.current_spend = {}
    
    def process_transaction(self, category, amount):

        try:
            # if category is "software", we can allow any amount
            if category == "software":
                self.current_spend[category] = amount + self.current_spend.get(category, 0)
                print(f"${amount} amount is UNDER spending cap for category: {category} --> APPROVED")
                print(f"Current Spend: {self.current_spend}")
                return

            # over the spending cap! 
            elif amount + self.current_spend.get(category, 0) > self.category_caps[category]:
                print(f"${amount} amount is OVER spending cap for category: {category} --> DENIED")
                print(f"Current Spend: {self.current_spend}")
                return None
            
            # if under the spending cap, we approve and add the amt:
            self.current_spend[category] = amount + self.current_spend.get(category, 0)
            print(f"${amount} amount is UNDER spending cap for category: {category} --> APPROVED")
            print(f"Current Spend: {self.current_spend}")
            return
        except ValueError:
            return None

    def process_transaction_better(self, category, amount):

        # normalize casing, if input comes as capitlized or something else:
        category = category.lower()

        # extract current accumulation state:
        current_total = self.current_spend.get(category, 0.0)
        projected_total = current_total + amount

        # 3: Guard Clause: Enforce strict budget constraints 
        # Check if the category has a cap rule AND if our projection breaches it. 
        if category in self.category_caps and projected_total > self.category_caps[category]:
            # The exception rule:
            if category != "software":
                print(f"❌ [DENIED] ${amount:.2f} is OVER cap for {category}. Current: ${current_total:.2f} | Limit: ${self.category_caps[category]:.2f}")
                return "DENIED"

        # 4. Single Path of Truth: If we clear the guard clause, mutate state permanently. 
        self.current_spend[category] = projected_total
        print(f"✅ [APPROVED] ${amount:.2f} added to {category}. New Total: ${projected_total:.2f}")
        return "APPROVED"

# test

if __name__ == "__main__":
    engine = RampSpendCapEngine()
    print("---------Testing-Spend-Engine---------")
    
    # First few travel expenses should pass: 
    engine.process_transaction("travel", 3000)
    engine.process_transaction("travel", 1500) 
    engine.process_transaction("travel", 1000) # should be declined: over the spending cap
    engine.process_transaction("software", 20000)





        

        