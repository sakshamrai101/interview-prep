"""
Rules

- The Ingestion Target: You are handed a list of corporate application records. Each has a company_name and a string verification_status which can be 
  "VERIFIED", "REVIEW_REQUIRED", or "SUSPICIOUS".

- The Status Label Mapping: * If verification_status is "VERIFIED", the label is "approved". 
  If verification_status is "REVIEW_REQUIRED", the label is "pending". If verification_status is "SUSPICIOUS", 
  the label is "flagged".

- The Guard Requirement: Start with a completely empty standard dictionary ({}). 
  Use your single-expression .get() pattern to dynamically initialize and increment the count of logs in 
  each respective compliance tier.

"""

class KYCComplianceAuditor:
    def __init__(self):
        # A flat stream of newly submitting businesses registering for corporate credit cards
        self.application_stream = [
            {"company_name": "Alpha Corp", "verification_status": "VERIFIED"},        # approved
            {"company_name": "Beta LLC",   "verification_status": "REVIEW_REQUIRED"}, # pending
            {"company_name": "Gamma Inc",  # flagged
             "verification_status": "SUSPICIOUS"},      
            {"company_name": "Delta Tech", "verification_status": "VERIFIED"},        # approved
            {"company_name": "Zeta Ventures", "verification_status": "VERIFIED"},    # approved
        ]

    def tally_compliance_statuses(self):

        application_status_counts = {}

        for stream in self.application_stream:
            if stream["verification_status"] == "VERIFIED":
                label = "approved"
            elif stream["verification_status"] == "REVIEW_REQUIRED":
                label = "pending"
            else:
                label = "flagged"
            
            application_status_counts[label] = application_status_counts.get(label, 0.0) + 1
        
        return application_status_counts

# ---- EXECUTION HARNESS ----
if __name__ == "__main__":
    auditor = KYCComplianceAuditor()
    print("---------Testing-KYC-Compliance-Auditor---------")
    
    report = auditor.tally_compliance_statuses()
    print("Final Compliance Status Tally Object:")
    print(report)
    # Expected output exactly: {'approved': 3, 'pending': 1, 'flagged': 1}