"""
    PROBLEM: SOP State Traversal Engine 

    CONTEXT: 
    Process an insurance claim through a decision tree from start_node to a terminal step,
    recording the path and checking for cycles.

    Input:

    workflow = {
    "CLAIM_RECEIVED": [
        {"target": "HIGH_VALUE_AUDIT", "condition_field": "claim_amount", "op": ">", "value": 5000},
        {"target": "STANDARD_REVIEW", "condition_field": "claim_amount", "op": "<=", "value": 5000}
    ],
    "HIGH_VALUE_AUDIT": [
        {"target": "LEGAL_HOLD", "condition_field": "has_fraud_flag", "op": "==", "value": True},
        {"target": "SENIOR_APPROVAL", "condition_field": "has_fraud_flag", "op": "==", "value": False}
    ],
    "STANDARD_REVIEW": [],
    "LEGAL_HOLD": [],
    "SENIOR_APPROVAL": []
}

claim = {"claim_amount": 7500, "has_fraud_flag": False}

Expected Output:
    {
      "path": ["CLAIM_RECEIVED", "HIGH_VALUE_AUDIT", "SENIOR_APPROVAL"],
      "terminal_node": "SENIOR_APPROVAL",
      "cycle_detected": False
    }

"""

class SOPGraphEngine:

    def __init__(self, workflow: dict):
        self.workflow = workflow
    
    def get_traversal_path(start_node: str, claim: dict) -> dict:


        if start_node not in self.workflow:
            raise ValueError(f"Start node '{start_node}' does not exist in workflow definition")
        
        path = []
        visited_nodes = set() # to detect cycles 
        current_node = start_node # use to traverse graph

        while current_node:
            
            # Step 1: Cycle Detection Step
            if start_node in visited_nodes:
                print(f"Cycle detected for 'claim': {claim} with 'start_node': {start_node}")
                return
            
            # Step 2: Record State 
            visited_nodes.add(current_node)
            path.append(current_node)

            # Step 3: Fetch the actual outgoing transaction:
            transition = self.workflow.get(current_node, [])



            next_node = None

        
            # Evaluate Transitions 
            for edge in transition:
                target = edge.get("target")
                field_name = edge.get("condition_field")
                op = edge.get("op")
                target_value = edge.get("value")

                field_value = claim.get(field_name)

                if self.eval_op(op, field_value, target_value):
                    next_node = target
                    break
        
        # Step 5: Advance Traversal
        current_node = next_node
        return path 

    def eval_op(self, op: str, val1, val2) -> bool: 
        """ Helper to evaluate operator string dynamically """
        if not val1:
            return False
        
        if op == ">": return val1 > val2
        if op == "<": return val1 < val2
        if op == ">=": return val1 >= val2
        if op == "<=": return val1 <= val2
        if op == "==": return val1 == val2
        if op == "in": return val1 in val2
    