from collections import deque 

"""
    PROBLEM: Multi-Section Rule Collector


Context:
    Enterprise SOP definitions are stored in deeply nested section hierarchies (sections contain sub-sections, 
    which contain more sub-sections). You need to search the entire section tree to find and collect all rules matching specific 
    query criteria, regardless of how deep they are nested.


nested_config = {
    "section_id": "SEC-ROOT",
    "rules": [
        {"id": "R1", "name": "KYC Check", "priority": 10},
        {"id": "R2", "name": "Basic Fraud", "priority": 3}
    ],
    "sub_sections": [
        {
            "section_id": "SEC-FINANCE",
            "rules": [
                {"id": "R3", "name": "AML Scan", "priority": 8}
            ],
            "sub_sections": [
                {
                    "section_id": "SEC-WIRE",
                    "rules": [
                        {"id": "R4", "name": "Wire Limit", "priority": 2},
                        {"id": "R5", "name": "OFAC Sanctions", "priority": 10}
                    ],
                    "sub_sections": []
                }
            ]
        }
    ]
}

Query: min_priority = 8

Expected Output (rules where priority >= 8):
 [
     {"id": "R1", "name": "KYC Check", "priority": 10},
     {"id": "R2" was skipped because 3 < 8},
     {"id": "R3", "name": "AML Scan", "priority": 8},
     {"id": "R5", "name": "OFAC Sanctions", "priority": 10}
 ]
"""

class SOPRuleSearcherEngine:

    def __init__(self, config: dict):
        self.config = config
    
    
    def find_rules_by_min_priority(self, min_priority: int) -> dict:
        if not self.config:
            return []

        q = deque([self.config])
        result = []

        while q:
            current_section = q.popleft()
            

            # Step 1: Filter rules in this section 
            for rule in current_section.get("rules", []):
                if rule.get("priority", 0) >= min_priority:
                    result.append(rule)

            # Step 2: Push Child sections onto queue for future loop iterations 
            for sub in current_section.get("sub_sections", []):
                q.append(sub)
        
        return result 

