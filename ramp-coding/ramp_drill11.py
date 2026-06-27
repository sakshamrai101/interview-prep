"""
Rules 

- The Ingestion Target: You are handed a list of user profile dictionaries. Each user has a username and a boolean flag is_active.

- The Counting Aggregation: Using a standard Python dictionary ({}), you must parse the stream and return a count of how many users 
are active vs. inactive.

- The Guard Requirement: You must use the .get() pattern we just discussed to increment your counts safely without causing a KeyError.

"""

class OnboardingAuditor:
    def __init__(self):
        # A flat stream of newly registered corporate card holders
        self.user_stream = [
            {"username": "saksham", "is_active": True},
            {"username": "disha",   "is_active": True},
            {"username": "bob",     "is_active": False},
            {"username": "alice",   "is_active": True},
            {"username": "charlie", "is_active": False},
        ]

    def tally_user_statuses(self):
        """
        YOUR TURN, BRO:
        1. Initialize a normal dict: status_counts = {}
        2. Loop through self.user_stream.
        3. Evaluate if 'is_active' is True or False. Set a string label: "active" or "inactive".
        4. Use status_counts[label] = status_counts.get(label, 0) + 1 to increment the counters safely.
        5. Return the status_counts dictionary.
        """

        status_counts = {}

        for stream in self.user_stream:
            if stream["is_active"]:
                label = "active"

            else:
                label = "inactive"
            status_counts[label] = status_counts.get(label, 0.0) + 1
        
        return status_counts


# ---- EXECUTION HARNESS ----
if __name__ == "__main__":
    auditor = OnboardingAuditor()
    print("---------Testing-Onboarding-Auditor---------")
    
    counts = auditor.tally_user_statuses()
    print("Final Status Tally Object:")
    print(counts)
    # Expected output exactly: {'active': 3, 'inactive': 2}