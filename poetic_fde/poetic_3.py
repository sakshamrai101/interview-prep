"""
Problem 3: SOP State Taversal Engine 

Context:

Poetic converts enterprise SOPs into executable graph workloads. You are given a workflow graph where nodes 
represent Process Steps and edges represent Conditional Transitions. 


Task:

Implement a function find_execution_path(workflow: dict, start_node: str, transaction_data: dict) -> list[str] 
that traverses the graph starting from start_node and returns the 
ordered list of node IDs visited until reaching a terminal node 
(a node with no outgoing edges or where no conditions pass).

workflow = {
    "START": [
        {"target": "VERIFY_IDENTITY", "condition_field": "amount", "op": ">", "value": 1000},
        {"target": "AUTO_APPROVE", "condition_field": "amount", "op": "<=", "value": 1000}
    ],
    "VERIFY_IDENTITY": [
        {"target": "FLAG_RISK", "condition_field": "is_new_user", "op": "==", "value": True},
        {"target": "MANUAL_REVIEW", "condition_field": "is_new_user", "op": "==", "value": False}
    ],
    "AUTO_APPROVE": [],
    "FLAG_RISK": [],
    "MANUAL_REVIEW": []
}

# Example Transaction
tx1 = {"amount": 1500, "is_new_user": True}
# Expected Path: ["START", "VERIFY_IDENTITY", "FLAG_RISK"]

"""

class SOPWorkflowEngine:

    def __init__(self, workflow: dict):
        """
        Constructor to initialise workflow engine with graph schema:

        {
            "Node_Name"": [
                {"target": "Next_Node", "condition_field": "field_name", "op": ">", "value": 100}
            ]
        }
        """
        self.workflow = workflow
    
    def eval_condtion(self, field_value, op: str, target_value) -> bool:
        """ Helper to safely evaluate dynamic string operators """
        if field_value is None:
            return False 
        
        if op == ">": return field_value > target_value
        if op == "<": return field_value < target_value 
        if op == ">=": return field_value >= target_value 
        if op == "<=": return field_value <= target_value 
        if op == "==": return field_value == target_value
        if op == "!=": return field_value != target_value 
        if op =="in": return field_value in target_value 
        return False 
    
    def find_execution_path(self, start_node: str, transaction_data: dict) -> list[str]:
        """
        Traverses the graph iteratively from start_node to terminal_node.
        Includes cycle detection via a visted set.

        """

        if start_node not in self.workflow:
            raise ValueError(f"Start node '{start_node}' does not exist in workflow definition")
        
        path = []
        visted_nodes = set()
        current_node = start_node
        cycle_detected = False

        while current_node:

            # Step 1: Cycle Detection Step
            if current_node in visted_nodes:
                cycle_detected = True
                print(f"[WARNING]: Cycle detected at node: '{current_node}'. Stopping traversal.")
                break 
            
            # Step 2: Record State
            path.append(current_node)
            visted_nodes.add(current_node)

            # Step 3: Fetch outgoing transitions:
            transitions = self.workflow.get(current_node, [])

            next_node = None
            # Step 4: Evaluate Transitions (First Match Wins)
            for edge in transitions:
                target = edge.get("target")
                op = edge.get("op")
                field_name = edge.get("condition_field")
                target_value = edge.get("value")

                field_value = transaction_data.get(field_name)

                if self.eval_condtion(field_value, op, target_value):
                    next_node = target
                    break
            
            # Step 5: Advance Traversal 
            current_node = next_node
        
        terminal_node = path[-1] if path else None
        return {
            "path": path,
            "terminal_node": terminal_node,
            "cycle_detected": cycle_detected
        } 
if __name__ == "__main__":
    workflow_schema = {
        "START": [
            {"target": "VERIFY_IDENTITY", "condition_field": "amount", "op": ">", "value": 1000},
            {"target": "AUTO_APPROVE", "condition_field": "amount", "op": "<=", "value": 1000}
        ],
        "VERIFY_IDENTITY": [
            {"target": "FLAG_RISK", "condition_field": "is_new_user", "op": "==", "value": True},
            {"target": "MANUAL_REVIEW", "condition_field": "is_new_user", "op": "==", "value": False}
        ],
        "AUTO_APPROVE": [],
        "FLAG_RISK": [],
        "MANUAL_REVIEW": []
    }

    engine = SOPWorkflowEngine(workflow=workflow_schema)

    print("--- Running Workflow Test Suite ---")

    # Test 1: High amount (>1000) & New User
    tx1 = {"amount": 1500, "is_new_user": True}
    res1 = engine.find_execution_path(start_node="START", transaction_data=tx1)
    print("Test 1 Result (Expected: ['START', 'VERIFY_IDENTITY', 'FLAG_RISK']):")
    print(f"  -> {res1}\n")

    # Test 2: Low amount (<=1000)
    tx2 = {"amount": 500, "is_new_user": False}
    res2 = engine.find_execution_path(start_node="START", transaction_data=tx2)
    print("Test 2 Result (Expected: ['START', 'AUTO_APPROVE']):")
    print(f"  -> {res2}\n")

    # Test 3: High amount (>1000) & Existing User
    tx3 = {"amount": 2500, "is_new_user": False}
    res3 = engine.find_execution_path(start_node="START", transaction_data=tx3)
    print("Test 3 Result (Expected: ['START', 'VERIFY_IDENTITY', 'MANUAL_REVIEW']):")
    print(f"  -> {res3}\n")

