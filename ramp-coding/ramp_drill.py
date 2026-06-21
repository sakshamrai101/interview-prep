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





