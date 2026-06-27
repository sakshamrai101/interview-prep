"""
RAMP NESTED MAPPING:

Rules:

- Dynamic Ingestion (log_charge): Process incoming logs containing company_id, department, employee_id, 
  and the charge amount. You must insert this data into a nested map structure.

- The Guard Trap: If a company or department has never been seen before, trying to access it 
  directly will throw a fatal KeyError. You must initialize nested dictionaries safely 
  on the fly (or use Python's collections.defaultdict).

- The Aggregation Query (get_department_total): Implement a high-speed method that 
  instantly returns the total historical spend for an entire 
  department inside a specific company.
"""

from collections import defaultdict

class RampNestedLedger:

    def __init__(self):

        self.ledger = defaultdict(lambda: defaultdict(list))

        # self.ledger[company_id][department] = list of charge amounts float
    
    def log_charge(self, company_id, department, employee_id, amount):

        """
        TASK:
        - Normalize the company_id and department strings to lowercase 
        - Append the amt directly into the nested list structure:
        self.ledger[company_id][department] 

        """

        amount = amount
        company_id = company_id.lower()
        department = department.lower()
        employee_id = employee_id.lower()

        self.ledger[company_id][department].append(amount)
    
    def get_department_total(self, company_id, department):
        company_id = company_id.lower()
        department = department.lower()



        # will run in O(n^2)

        
        # for company in self.ledger:
        #     if company == company_id:
        #         for internal_department in self.ledger[company]:
        #             if internal_department == department:
        #                 for amount in self.ledger[company][internal_department]:
        #                     deparment_spend += amount
        if company_id in self.ledger and department in self.ledger[company_id]:
            return sum(self.ledger[company_id][department])
        
        return 0.0

# ---- THE EVALUATION HARNESS ----
if __name__ == "__main__":
    engine = RampNestedLedger()
    print("---------Testing-Nested-Relational-Mapping---------")
    
    # Ingesting flat stream events
    engine.log_charge("Ramp", "Engineering", "emp_1", 1200.00)
    engine.log_charge("Ramp", "Engineering", "emp_2", 800.00)
    engine.log_charge("Ramp", "Marketing", "emp_3", 500.00)
    engine.log_charge("Stripe", "Engineering", "emp_4", 3000.00) # Different Company!
    
    # Querying aggregations
    ramp_eng_total = engine.get_department_total("Ramp", "Engineering")
    ramp_mkt_total = engine.get_department_total("Ramp", "Marketing")
    stripe_eng_total = engine.get_department_total("Stripe", "Engineering")
    
    print(f"Ramp Engineering Total Spend: ${ramp_eng_total:.2f}") # Should be $2000.00
    print(f"Ramp Marketing Total Spend:   ${ramp_mkt_total:.2f}")   # Should be $500.00
    print(f"Stripe Engineering Total Spend: ${stripe_eng_total:.2f}") # Should be $3000.00
    
    # Guard Test: Querying a completely non-existent department
    unknown_total = engine.get_department_total("Ramp", "Sales")
    print(f"Ramp Sales Total Spend (Unknown): ${unknown_total:.2f}") #
                        






