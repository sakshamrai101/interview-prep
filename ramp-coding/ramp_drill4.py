# Paginated Ledger with Token-Bucket rate-limiting

import time 

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.status_code = status_code
        self.json_data = json_data
        self.text = str(json_data)

    def json(self): return self.json_data


class MockSensitiveServer:
    def __init__(self):
        self.last_request_time = 0
    
    def get(self, url, params=None):
        current_time = time.time()
        params = params or {}
        cursor = params.get("cursor")

        # Strict security constraint: Requests must be spaced at least 0.8 seconds apart
        if current_time - self.last_request_time < 0.8:
            return MockResponse({"error": "Rate limit tripped! Requests arrived too fast."}, status_code=429)
        
        self.last_request_time = current_time

        # Page 1
        if not cursor:
            return MockResponse({
                "records": [
                    {"id": "rec_1", "amount": "500.00", "status": "SETTLED"},
                    {"id": "rec_2", "amount": "250.50", "status": "PENDING"}
                ],
                "next_cursor": "page_2"
            })
        # Page 2
        elif cursor == "page_2":
            return MockResponse({
                "records": [
                    {"id": "rec_3", "amount": "1200.00", "status": "SETTLED"}
                ],
                "next_cursor": "page_3"
            })
        # Page 3
        elif cursor == "page_3":
            return MockResponse({
                "records": [
                    {"id": "rec_4", "amount": "bad_row", "status": "SETTLED"}
                ],
                "next_cursor": None
            })

requests = MockSensitiveServer()
BASE_URL = "https://api.internal-ramp.com/v1/settlements"

class RampSettlementCrawler:
    def __init__(self, base_url):

        self.base_url = base_url

        # 1. Financial State Tracker 
        self.total_settled_volume = 0.0

        # 2. Rate Limiter State Tracker 
        self.last_call_time = 0.0
        self.min_interval = 1.0 # Force a minimum of 1.0 second wait between network calls 

    
    def wait_for_token(self):
        """
        THE RATE LIMITER GUARD:

        Calculates how much time has passed since our last API call.
        If it's less than min_interval, it sleeps the thread to protect the bucket.

        """
        now = time.time()
        time_passed = now - self.last_call_time

        if time_passed < self.min_interval:
            sleep_needed = self.min_interval - time_passed
            print(f"[RATE-LIMIT] Backing off! Sleeping for {sleep_needed:.2f} seconds to refill token bucket....")
            time.sleep(sleep_needed)

        
        # Update our timestamp marker to right now:
        self.last_call_time = time.time()

    
    def fetch_page(self, cursor_value=None):
        """
        The Network Helper:
        Always calls wait_for_token before hitting requests.get to guarantee compliance.
    
        """

        self.wait_for_token()

        query_params = {}
        if cursor_value:
            query_params["cursor"] = cursor_value
        print(f"Making safe call to endpoint with cursor: {cursor_value}")
        response = requests.get(self.base_url, params=query_params)
        print(f"Server response code: {response.status_code}")

        if response.status_code == 429:
            print(f"Hitting 429, the rate limit logic is broken")
            return None 
        
        if response.status_code != 200:
            print(f"Failed call with status: {response.status_code}")
            return None 
        
        return response.json()
    

    def parse_and_accumulate(self, record):
        """
        THE DATA CLEANER:

        Safely extracts amount if data is settled.

        """
        status = record.get("status")
        raw_amount = record.get("amount")

        if status != "SETTLED":
            return
        
        try:
            amount_float = float(raw_amount)
            self.total_settled_volume += amount_float
            print(f"  [MATH] Added ${amount_float:.2f} | Current running volume: ${self.total_settled_volume:.2f}")
        except (ValueError, TypeError):
            print(f"  [DATA WARNING] Corrupt amount value found: '{raw_amount}'. Skipping row.")

    def run(self):
        """
        THE BOSS FUNCTION:

        Orchestrates the entire pagination timeline loop. 

        """

        current_cursor = None 
        keep_crawling = True

        while keep_crawling:
            page_payload = self.fetch_page(cursor_value=current_cursor)

            # Guard Rule: If network layer breaks, stop
            if not page_payload:
                print("Network failure detected. Shutting down loop.")
                break
            
            records_list = page_payload.get("records", [])
            print(f" Ingested {len(records_list)} rows from current page. Routing to data cleaner ....")

            # Step C:
            for row in records_list:
                self.parse_and_accumulate(row)

            
            # Advance our pagination pointer
            next_page_pointer = page_payload.get("next_cursor")

            if next_page_pointer:
                # If cursor string exists, update current_cursor for the next iteration 
                current_cursor = next_page_pointer
            else:
                # If next cursor is None, we have reached the last page! Stop the machine cleanly. 
                keep_crawling = False
                print("No more pagination cursors found")

if __name__ == '__main__':
    crawler = RampSettlementCrawler(BASE_URL)
    crawler.run()
    


        
