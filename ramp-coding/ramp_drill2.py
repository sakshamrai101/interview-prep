import time

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.text = str(json_data)
    def json(self): return self.json_data

class MockRequestsSession:
    def __init__(self):
        self.api_calls = 0

    def get(self, url, params=None):
        params = params or {}
        token = params.get("page_token")
        
        # Page 1 (Initial call - no token)
        if not token:
            return MockResponse({
                "expenses": [
                    {"expense_id": "exp_1", "employee": "Alice", "department": "Engineering", "amount": 150.00, "category": "Software"},
                    {"expense_id": "exp_2", "employee": "Bob", "department": "Sales", "amount": 4500.00, "category": "Travel"},
                    {"expense_id": "exp_3", "employee": "Charlie", "department": "Engineering", "amount": "corrupt_null", "category": "Software"}
                ],
                "next_page_token": "token_page_2"
            })
            
        # Page 2 (Last Page)
        elif token == "token_page_2":
            return MockResponse({
                "expenses": [
                    {"expense_id": "exp_4", "employee": "David", "department": "Sales", "amount": 3200.00, "category": "Entertainment"},
                    {"expense_id": "exp_5", "employee": "Eve", "department": "Marketing", "amount": 250.00, "category": "SaaS"}
                ],
                "next_page_token": None
            })
            
        return MockResponse({"error": "Invalid token"}, status_code=400)

# Globally patch 'requests' for our workspace
requests = MockRequestsSession()
BASE_URL = "https://api.internal-ramp.com/v1/expenses"



"""
Ramp allows companies to issue corporate cards to employees. 
To prevent fraud, you need to build an automated audit script that checks an API for transaction logs, 
flags expenses that breach company policy, and counts how many violations occurred per department.

"""
class RampExpenseAuditor:

    # Idea of the constructor is to initialize 
    def __init__(self, start_url):
        self.api_url = self.start_url

        # Tracking dictionary 
        self.department_violations = {}
    
    def fetch_page_json(self, token_value=None):
        query_params = {}
        if token_value:
            query_params["next_page_token"] = token_value
        
        # Actually make the api call:
        response = requests.get(self.api_url, query_params)

        print(f"Response came back with status code: {response.status_code}")

        # Handle 429, rate-limit error 
        if response.status_code == 429:
            print("Hitting rate-limit error, waiting for 1 second before exiting ......")
            time.sleep(1)
            return None
        
        # Server errors: 500, 404 or something
        if response.status_code != 200:
            return None
        
        # If everything is fine we return json data
        return response.json()
    

    def check_single_transaction(self, expense_row):
        expense_id = expense_row.get("expense_id")
        department = expense_row.get("department")
        raw_amount = expense_row.get("amount")


        try:
            # Convert string to floats:
            clean_amount = float(raw_amount)

            # return clean tupple 
            return department
        except (ValueError, TypeError):
            # This catches corrupt text rows (like "invalid amount corrupted")
            print(f"Transaction {expense_id} has unparseable amount: '{raw_amount'. Skipping now.}")
            return None 
        
    
    def run_audit(self):
        """
        Orchestrates the pagination loops and aggregates the policy voilation counts. 
        """

        current_token = None
        keep_loading = True 

        while keep_loading:
            # 1. Fetch the page data for the current page:
            page_result = self.fetch_page_json(token_value=current_token)
            if not page_data:
                # Halting api call right now as hit some network error
                break
            
            # 2. Extract array 
            expenses_list = page_data.get("expenses", [])
            print(f"Processing {len(expenses_list)} expenses on this page ....")

            # 3. Clean and inpsect each row 
            for row in expenses_list:
                violated_department = self.check_single_transaction(row)

                # If a violation department was returned, update our tracking state
                if violated_department:
                    if violated_department not in self.department_violations:
                        self.department_violations[violated_department] = 0
                    
                    self.department_violations[violated_department] += 1
                
            
            # 4. Advance pagination token:
            next_token = page_data.get("next_cursor_token")
            if next_token:
                current_token = next_token
            else:
                keep_loading = False
                print(f"Reached the final page of records cleanly")

    # 5. Output the final system output 
    for dept, count in self.department.violations.items():
        print(f" * {dept}: {count} violation(s)")


