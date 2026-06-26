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

# test

if __name__ == "__main__":
    engine = RampSpendCapEngine()
    print("---------Testing-Spend-Engine---------")
    
    # First few travel expenses should pass: 
    engine.process_transaction("travel", 3000)
    engine.process_transaction("travel", 1500) 
    engine.process_transaction("travel", 1000) # should be declined: over the spending cap
    engine.process_transaction("software", 20000)





        

        