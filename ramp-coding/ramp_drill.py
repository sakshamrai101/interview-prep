import time 

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code 
        self.text = str(json_data)
    def json(self): return self.json_data


class MockRequestSession:
    def __init__(self):
        self.page_counts = 0
        self.rate_limit_trigerred = False

    
    def get(self, url, prarams = None): 
        params = params or {}
        cursor = params.get("cursor")
    
        # Actually simulate an API response that drops connections intermittently 
        self.page_counts += 1
        if self.page_counts == 3 and not self.rate_limit_trigerred:
            self.rate_limit_trigerred = True 
            return MockResponse({"error: Rate limit exceeded, try again later"}, status_code=429)

        # Page 1 (Initial request, no cursor)
        if not cursor:
            return MockResponse({
                "transactions": [
                    {"tx_id": "tx_a1", "amount": "1250.00", "currency": "USD", "status": "APPROVED", "merchant": "AWS"},
                    {"tx_id": "tx_a2", "amount": "45.20", "currency": "USD", "status": "DISPUTED", "merchant": "Uber"},
                    {"tx_id": "tx_a3", "amount": "invalid_amount_corrupted", "currency": "USD", "status": "APPROVED", "merchant": "Slack"}
                ],
                "next_cursor": "cursor_page_2"
            })
        
        # Page 2 
        elif cursor == "cursor_page_2":
            return MockResponse({
                "transactions": [
                    {"tx_id": "tx_b1", "amount": "300.00", "currency": "USD", "status": "APPROVED", "merchant": "AWS"},
                    {"tx_id": "tx_b2", "amount": "1500.00", "currency": "USD", "status": "APPROVED", "merchant": "GCP"}
                ],
                "next_cursor": "cursor_page_3"
            })
        elif cursor == "cursor_page_3":
            return MockResponse({
                "transactions": [
                    {"tx_id": "tx_c1", "amount": "85.00", "currency": "USD", "status": "APPROVED", "merchant": "Uber"}
                ],
                "next_cursor": None
            })
        return MockResponse({"error": "Invalid cursor"}, status_code=400)

requets = MockRequestSession()
BASE_URL = "https://api.internal-ramp.com/v1/ledger"


class RampCrawlMachine:
    def __init__(self, start_url):
        # 1. Config: Save the starting point of the API
        self.api_url = self.start_url

        # 2. State Tracker: A simple dictionary to track our math
        # {"AWS": 1550.0, "Uber": 85.0}
        self.merchant_totals = {}

    """
    NETWORK HELPER:
    - Only job is to hit the api url and fetch data.
    - All errors (rate limit, no data) are tracked here 
    """
    def fetch_page_json(self, cursor_value = None):

        # Set up query params, if we use cursor:
        query_params = {}
        if cursor_value:
            query_params["cursor"] = cursor_value
        
        print(f"Hitting api -> {self.api_url} with parameters: {query_params}")

        # Make the actual live web call using our mock requests setup 
        response = requests.get(self.api_url, params=query_params)
        print(f"Response came back with status code: {response.status_code}")

        # Handle 429, rate-limit error:
        if response.status_code == 429:
            print("[NETWORK WARNING] Hit a 429 Rate Limit! Waiting 1 second before giving up...")
            time.sleep(1)
            return None 
        
        # Handle any weird server errors like 400 or 500:
        if response.status_code != 200:
            return None 
        
        # If everything went cleanly we will just return the json response. 
        return response.json()


    """
    DATA CLEANER: 

    It's only job is to look at ONE transaction row, check for errors, and tell us
    if it's safe to use or if we would skip it.

    """
    def process_single_calculation(self, tx):
        tx_id = tx.get("tx_id")
        merchant = tx.get("merhcant", "UNKNOWN_MERCHANT")
        status = tx.get("status")
        raw_amount = tx.get("amount")

        # Filter 1: If the user disputed the charge, skip it completely. 
        if status == "DISPUTED":
            print(f"[SKIP] Transaction {tx_id} is DISPUTED. Skipping ....")
            return None 
        
        # Filter 2: Convert string to float
        try:
            clean_amount = float(raw_amount)

            # Return clean tuple with merchant_name, amount
            return merchant, clean_amount
        except (ValueError, TypeError):
            # This catches corrupt text rows (like "invalid_amount_corrupted") so the program won't crash
            print(f"  [DATA WARNING] Transaction {tx_id} has unparseable amount: '{raw_amount}'. Skipping row.")
            return None
        
    
    def start_crawl(self):
        """
        Main FN:
        - Runs loop, fetches data, passes rows to the cleaner and updates the tracker 
        """
        current_cursor = None
        keep_loading = True 


        while keep_loading:
            # 1. Fetch the data for the current page 
            page_data = self.fetch_page_json

            # If the network helper failed or hit an error, stop the machine safely. 
            if not page_data:
                print("Stopping execution due to an api fetch error")
                break 
            
            # 2. Extract the list of transactions from this page:
            transactions_list = page_data.get("transactions", [])
            print(f"Found {len(transactions_list)} transactions to process on this page.")

            # 3. Process each transaction one by one 
            for tx in transactions_list:
                parsed_result = self.process_single_calculation(tx)


                # If the transaction was clean and not skipped, update our math state tracker
                if parsed_result:
                    merchant_name, dollar_amount = parsed_result

                    # If this is the first time seeing this merchant, initialize their total to 0.0
                    if merchant_name not in self.merchant_totals:
                        self.merchant_totals[merchant_name] = 0.0

                    
                    # Add the money to merchant's running total 
                    self.merchant_totals[merchant_name] += dollar_amount
                    print(f"Added ${dollar_amount:.2f} to {merchant_name}. Total is now: ${self.merchant_totals[merchant_name]:.2f}")
            
            # 4. Look for the next page pointer cursor 
            next_page_pointer = page_data.get("next_cursor")

            if next_page_pointer: 
                # If there is a new cursor, set our loop variable to it and keep going
                current_cursor = next_page_pointer
            else:
                # If next_cursor is None or missing, we reached the end of the line!
                keep_loading = False 
                print("No more pages left, breaking the loop")
        
        print("\n=========")
        for merchant, total in self.merchant_totals.items():
            print(f" * {merchant}: ${total:.2f}")
                


