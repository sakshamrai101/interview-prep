"""
Multi Currency Payment Ledger 

Interviewer: *"Welcome, Saksham. At Ramp, we process transactions globally. 
A recurring issue in distributed financial systems is network retries. 
If a client hits buy, the request times out, and they hit buy again, we cannot charge them twice.

Your task is to design an in-memory Idempotent Payment Processor Engine. 
It needs to accept incoming transaction requests, deduplicate them using an idempotency_key, convert currencies on 
the fly using a dynamic conversion lookup table, and return a running ledger statement of net settled volumes per currency."*

"""

class IdempotentPaymentEngine:

    def __init__(self):

        # 1. Stores: {idempotency_key -> transaction_response_dictionary}
        self.processed_keys = {}

        # 2. Dictionary to store core ledger volume per unique currency symbol.
        self.ledger = {}

        # 3. Setup static exchange rates relative to USD (BASE CURRENCY).
        self.exchange_rates = {
            "USD": 1.0,
            "EUR": 1.10,
            "GBP": 1.30
        }
    
    def process_transaction(self, idempotency_key: str, amount: float, currency: str, action: str) -> dict:
        """
        Processes an incoming corporate spend event safely and returns a status receipt. 

        """

        # --- LAYER 1: IDEMPOTENCE CHECK ---
        # Before executing any math, we immediately check our deduplication map.
        if idempotency_key in self.processed_keys:
            print(f"[IDEMPOTENCY KEY DETECTED]: Key {idempotency_key} detected. Returning chache response")
            return self.processed_keys[idempotency_key]

        
        # --- LAYER 2: VALIDATION GUARD ---
        # Verify if the currency exists inside our system profile 
        if currency not in self.exchange_rates:
            return {"status": "REJECTED", "error": f"Invalid ledger action: {action}"}
        

        # --- LAYER 3: STATE MUTATION & MATH ---
        # Determine the polarity of the money movement based on the transaction action type 
        if action == "CHARGE":
            modifier = 1
        elif action == "REFUND":
            modifier = -1
        else:
            return {"status": "REJECTED", "error": f"invalid ledger action: {action}"}
        
        # Compute the final delta to apply to the currency bucket 
        delta = amount * modifier 

        # Safely increment the running ledger total using our signature .get() pattern
        self.ledger[currency] = self.ledger.get(currency, 0.0) + delta 


        # --- LAYER 4: RESPONSE GENERATION & CACHING ---
        # Build the immutable receipt artifact 
        receipt = {
            "status": "SETTLED",
            "net_data": delta,
            "currency": currency
        }

        # Save this receipt artifact directly inside our idempotence cache 
        self.processed_keys[idempotency_key] = receipt

        # Return the newly generated receipt back to the caller
        return receipt
    
    def get_total_volume_in_usd(self) -> float:
        """
        Aggregates all multi-currency ledger balances into a single consolidted usd total.
        """
        total_usd = 0.0

        for currency, balance in self.ledger.items():
            total_usd += balance * self.exchange_rates[currency]
        
        return total_usd
if __name__ == "__main__":
    engine = IdempotentPaymentEngine()
    print("--------- Testing Idempotent Multi-Currency Ledger ---------")

    # Transaction 1: Standard charge of 100 EUR
    res1 = engine.process_transaction("tx_req_001", 100.00, "EUR", "CHARGE")
    print(f"Initial Request Result: {res1}") # Expect SETTLED, delta +100

    # Transaction 2: SIMULATED NETWORK RETRY. Same payload, same key.
    res2 = engine.process_transaction("tx_req_001", 100.00, "EUR", "CHARGE")
    print(f"Retried Request Result: {res2}") 
    
    # Assert that the system did NOT add another 100 EUR to the ledger
    assert engine.ledger["EUR"] == 100.00, f"Deduplication Failure! Expected 100.00 EUR, got {engine.ledger['EUR']}"
    print(" ✅ Network retry safely de-duplicated via Idempotency cache.")

    # Transaction 3: Process a refund of 50 GBP
    engine.process_transaction("tx_req_002", 50.00, "GBP", "CHARGE")
    engine.process_transaction("tx_req_003", 10.00, "GBP", "REFUND") # Net GBP should be 40
    assert engine.ledger["GBP"] == 40.00

    # Calculate Total Portfolio Valuation in USD
    # (100 EUR * 1.10) + (40 GBP * 1.30) -> 110.00 + 52.00 = 162.00
    total_valuation = engine.get_total_volume_in_usd()
    print(f"Total Portfolio Valuation: ${total_valuation:.2f} USD")
    assert total_valuation == 162.00

    print("\n🏁 [SUCCESS] Problem 1 cleared! Ready for the next problem.")