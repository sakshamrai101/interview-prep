"""
Multi - Currency Ledger:

- The Exchange Table: Your code must look up the correct multiplier from self.exchange_rates.

- Defensive Validation: If an employee passes an invalid or unsupported currency type (like "EUR"), 
  your system must log an error and return False without crashing or updating any totals.

- The State Mutation: Convert the raw amount to USD (usd_amount = raw_amount * rate), 
  add it to the running ledger volume, and increment the exact count of how many times that specific 
  currency has been used across the firm.
"""

class MultiCurrencyLedger:
    def __init__(self):

        # 1 unit of currency = X USD
        self.exchange_rates = {
            "usd": 1.00,
            "gbp": 1.30,  # 1 GBP = $1.30 USD
            "jpy": 0.0065 # 1 JPY = $0.0065 USD
        }

        # central state trackers 
        self.total_usd_volume = 0.0
        self.currency_counts = {} # format: {"USD": 1, "GBP": 2}
        
    
    def log_transaction(self, currency, raw_amount):

        # clean incoming currency string (upper/lower case)
        currency = currency.lower()

        if currency not in self.exchange_rates:
            print(f"[ERROR]: {currency} not in Exchange Range Register")
            return False
        
        amount_usd = self.exchange_rates[currency] * raw_amount

        # update running volume and usage count
        self.total_usd_volume += amount_usd
        self.currency_counts[currency] = self.currency_counts.get(currency, 0) + 1

        print(f"[SUCCESS]: {raw_amount} {currency} -> ${amount_usd}")
        return True 

if __name__ == "__main__":

    ledger = MultiCurrencyLedger()
    
# Executing transactional logs
    ledger.log_transaction("USD", 100.00)
    ledger.log_transaction("gbp", 10.00)   # Should add $13.00 USD, increment GBP count
    ledger.log_transaction("JPY", 10000.00) # Should add $65.00 USD, increment JPY count
    
    # Guard testing: This should hit your safety check and return False cleanly
    is_valid = ledger.log_transaction("EUR", 50.00) 
    print(f"Was EUR transaction handled safely? {is_valid}")
    
    print("\n--- FINAL LEDGER AUDIT ---")
    print(f"Total Converted USD Ledger Volume: ${ledger.total_usd_volume:.2f}")
    print(f"Currency Audit Metric Counts: {ledger.currency_counts}")
