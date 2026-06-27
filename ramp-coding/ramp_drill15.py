"""
Rules

- The Duplicate Catch: Employees often accidentally upload the exact same receipt twice. 
  You are given a stream of payment dictionaries.

- The Aggregation Mapping: Loop through self.raw_stream. If a vendor name has already been processed, 
  you must log that transaction as a duplicate and increment the "duplicate_attempts" count. If it is new, 
  increment the "unique_vendors" count.

- The Guard Requirement: Start with a completely empty standard dictionary ({}). Use the .get() 
  pattern to dynamically track both counters.

"""
class VendorDeDupEngine:
    def __init__(self):
        self.raw_stream = [
            {"tx_id": "t1", "vendor": "AWS"},
            {"tx_id": "t2", "vendor": "Slack"},
            {"tx_id": "t3", "vendor": "AWS"},   # Duplicate!
            {"tx_id": "t4", "vendor": "Google"},
            {"tx_id": "t5", "vendor": "Slack"}, # Duplicate!
        ]

    def audit_vendors(self):
        """
        YOUR TASK: Populate an empty dict tracking unique vs duplicate tallies using .get().
        Hint: You'll also want an internal set() or list to keep track of seen vendors!
        Expected Output: {'unique_vendors': 3, 'duplicate_attempts': 2}
        """

        has_seen = set()
        audit_counts = {}

        for stream in self.raw_stream:
            if stream["vendor"] in has_seen:
                label = "duplicate_attempts"
            else:
                has_seen.add(stream["vendor"])
                label = "unique_vendors"
            audit_counts[label] = audit_counts.get(label, 0.0) + 1
        
        return audit_counts

if __name__ == "__main__":
    engine = VendorDeDupEngine()
    print("---------Testing-Vendor-De-Duplication---------")
    
    report = engine.audit_vendors()
    print("Final Audit Report Tally:")
    print(report)
    
    # Assert checks to verify code behavior matches system spec requirements
    assert report.get("unique_vendors") == 3, f"Expected 3 unique vendors, got {report.get('unique_vendors')}"
    assert report.get("duplicate_attempts") == 2, f"Expected 2 duplicate attempts, got {report.get('duplicate_attempts')}"
    print("\n✅ [PASSED] De-duplication logic and tracking counts match perfectly!")
