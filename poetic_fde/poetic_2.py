"""
problem - 2

In-Memory Audit Ledger 

-> Implement a class AccountLedger that ingests events one by one via ingest_event(event: dict) -> dict or processes a 
   batch with process_batch(events: list[dict]) -> list[dict].

-> each event looks like (input format):
    {
    "event_id": "EVT-1001",
    "account_id": "ACC-55",
    "timestamp": 1700000000,  # Epoch seconds
    "action": "DEPOSIT",      # "CREATE_ACCOUNT", "DEPOSIT", "WITHDRAWAL", "FREEZE", "UNFREEZE"
    "amount": 150.00          # Optional depending on action
    }

-> Ledger Rules:

Initial State: An account starts with a balance of 0.0 and state "ACTIVE". If a DEPOSIT or WITHDRAWAL 
               comes in for an account that has not received a CREATE_ACCOUNT event, implicitly initialize the 
               account as "ACTIVE" with 0.0 balance before applying the action.

Transaction Rules:

DEPOSIT: Adds amount to the account's balance.

WITHDRAWAL: Subtracts amount from the account's balance.

Constraint: If a withdrawal exceeds the current balance, the transaction is FLAGGED_NSF (Non-Sufficient Funds), 
            and the balance is unaffected.

FREEZE: Changes account state to "FROZEN".

Constraint: While "FROZEN", any WITHDRAWAL or DEPOSIT must be FLAGGED_FROZEN, and the balance is unaffected.

UNFREEZE: Restores account state to "ACTIVE".



class AccountLedger:

    def __init__(self, events):
        self.balance = 0
        self.account_state = "ACTIVE"
        self.events = events
        self.status = ""
        self.accounts = []
    
    def process_transaction(self):

        for event in self.events:
            self.accounts.append(self.evaluate_transaction(event))
        
        return self.accounts
    
    def evaluate_transaction(self, event):
        event_id = event["event_id"]
        account_id = event["account_id"]
        action = event["action"]

        # Freeze
        if action == "FREEZE":
            self.account_state = "FROZEN"
        # UnFreeze
        elif action == "UNFREEZE":
            self.account_state = "ACTIVE"

        # Deposit
        elif action == "DEPOSIT":
            if self.account_state == "FROZEN":
                self.status = "FLAGGED_FROZEN"
            else:
                self.status = "PROCESSED"
                self.balance += event.get("amount", 0)
        
        # Withdrawal
        elif action == "WITHDRAWAL":
            if self.account_state == "FROZEN":
                self.status = "FLAGGED_FROZEN"
            else:
                amount_to_deduct = event.get("amount", 0)

                if amount_to_deduct > self.balance:
                    self.status = "FLAGGED_NSF" 
                else:
                    self.status = "PROCESSED"
                    self.balance -= event.get("amount", 0)
        
        # Account Create 
        elif action == "CREATE_ACCOUNT":
            self.account_state = "ACTIVE"
        
        return {
            "event_id": event_id,
            "account_id": account_id,
            "status": self.status,
            "current_balance": self.balance,
            "account_state": self.account_state
        }


if __name__ == "__main__":
    events = [
    {"event_id": "E1", "account_id": "A1", "timestamp": 100, "action": "CREATE_ACCOUNT"},
    {"event_id": "E2", "account_id": "A1", "timestamp": 101, "action": "DEPOSIT", "amount": 100.00},
    {"event_id": "E3", "account_id": "A1", "timestamp": 102, "action": "FREEZE"},
    {"event_id": "E4", "account_id": "A1", "timestamp": 103, "action": "WITHDRAWAL", "amount": 50.00}, # FLAGGED_FROZEN
    {"event_id": "E5", "account_id": "A1", "timestamp": 104, "action": "UNFREEZE"},
    {"event_id": "E6", "account_id": "A1", "timestamp": 105, "action": "WITHDRAWAL", "amount": 120.00}, # FLAGGED_NSF
    ]
    ledger = AccountLedger(events)
    print(ledger.process_transaction())


^^ THIS IS MY SOLUTION 
"""

class AccountLedger:

    def __init__(self):
        # Map account_id -> {"balance": float, "state": str}
        self.accounts = {}
    
    def create_or_get_account(self, account_id: str) -> dict:
        """ Implicitly creates account if it does not exist """
        if account_id not in self.accounts:
            self.accounts[account_id] = {
                "balance": 0.0,
                "state": "ACTIVE"
            }
        
        return self.accounts[account_id]
    
    def ingest_event(self, event: dict) -> dict:
        event_id = event["event_id"]
        account_id = event["account_id"]
        action = event["action"]
        amount = event.get("amount", 0.0)

        account = self.create_or_get_account(account_id)
        status = "PROCESSED"

        # 1. Check frozen condition first:
        if account["state"] == "FROZEN" and action in ("DEPOSIT", "WITHDRAWAL"):
            status = "FLAGGED_FROZEN"
        
        # Process actions if not blocked by freeze 
        elif action == "DEPOSIT":
            account["balance"] += amount 
        
        elif action == "WITHDRAWAL":
            if amount > account["balance"]:
                status = "FLAGGED_NSF"
            else:
                account["balance"] -= amount 
        
        elif action == "FREEZE":
            account["state"] = 'FROZEN'
        elif action == "UNFREEZE":
            account["state"] = "ACTIVE"
        elif action == "CREATE_ACCOUNT":
            account["state"] = "ACTIVE"
        

        return {
            "event_id": event_id,
            "account_id": account_id,
            "status": status,
            "current_balance": account["balance"],
            "account_balance": account["state"]
        }
    
    def process_batch(self, events: list[dict]) -> list[dict]:
        return [self.ingest_event(evt) for evt in events]

if __name__ == "__main__":
    events = [
        {"event_id": "E1", "account_id": "A1", "timestamp": 100, "action": "CREATE_ACCOUNT"},
        {"event_id": "E2", "account_id": "A1", "timestamp": 101, "action": "DEPOSIT", "amount": 100.00},
        {"event_id": "E3", "account_id": "A1", "timestamp": 102, "action": "FREEZE"},
        {"event_id": "E4", "account_id": "A1", "timestamp": 103, "action": "WITHDRAWAL", "amount": 50.00}, # FLAGGED_FROZEN
        {"event_id": "E5", "account_id": "A1", "timestamp": 104, "action": "UNFREEZE"},
        {"event_id": "E6", "account_id": "A1", "timestamp": 105, "action": "WITHDRAWAL", "amount": 120.00}, # FLAGGED_NSF
        # Multiple account check
        {"event_id": "E7", "account_id": "A2", "timestamp": 106, "action": "DEPOSIT", "amount": 200.00},
    ]

    ledger = AccountLedger()
    results = ledger.process_batch(events)
    for r in results:
        print(r)