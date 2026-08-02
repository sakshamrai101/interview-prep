from collections import defaultdict, deque
"""
    Problem: Automated Workflow Task Scheduler 

    Context: 
    In automated SOP execution, workflows consist of tasks where certain tasks cannot run until their dependent 
    prerequisite tasks complete. Your system needs to find a valid linear execution order for all tasks, 
    or detect if there is a circular dependency (deadlock) that prevents execution.


    Input & Output Sample:

Task ID mapped to list of Task IDs it DEPENDS ON
tasks_config = {
    "GENERATE_DOC": [],                     # Runs first (0 deps)
    "VERIFY_CREDIT": ["GENERATE_DOC"],      # Waiting on GENERATE_DOC
    "APPROVE_LOAN": ["VERIFY_CREDIT"],      # Waiting on VERIFY_CREDIT
    "DISBURSE_FUNDS": ["APPROVE_LOAN"]      # Waiting on APPROVE_LOAN
}

Expected Output (Valid Execution Order):
  {
      "status": "SUCCESS",
      "execution_order": ["GENERATE_DOC", "VERIFY_CREDIT", "APPROVE_LOAN", "DISBURSE_FUNDS"]
  }

  Cyclic / Deadlock Input Sample:
cyclic_tasks = {
    "STEP_A": ["STEP_C"],
    "STEP_B": ["STEP_A"],
    "STEP_C": ["STEP_B"]
}

  Expected Output (Deadlock Detected):
  {
      "status": "DEADLOCK_DETECTED",
      "execution_order": []
  }
"""

# We need to resolve dependencies so Kahn's Algorithm (In-Degree Tracking)
# In dependency graph, tasks might have multiple prereqs (task C needs both tasks A and tasks B)

class SOPTaskScheduler:

    def __init__(self, tasks_config):
        self.tasks_config = tasks_config 
    
    def get_execution_order(self) -> dict:

        # Step 1: Calculate in-degree (number of pending dependencies)
        # and build an adjacency list of downstream dependents 
        in_degree = {task: len(deps) for task, deps in self.tasks_config.items()}
        graph = defaultdict(list)

        for task, deps in self.tasks_config.items():
            for dep in deps:
                graph[dep].append(task) # dep -> downstream task waiting for it 
        
        # Step 2: Queue all tasks with 0 dependencies (ready to run)
        q = deque([task for task, count in in_degree.items() if count == 0])
        
        execution_order = []

        # Step 3: Process Ready Tasks
        while q:
            current_task = q.popleft()
            execution_order.append(current_task)

            # Decrement in-degree for downstream tasks waiting on current_task 
            for dependent_task in graph[current_task]:
                in_degree[dependent_task] -= 1

                # If all dependencies are cleared, add to queue 
                if in_degree[dependent_task] == 0:
                    q.append(dependent_task)

        
        # Step 4: Deadlock Check (if resolved count < total tasks, a cycle exists)
        if len(execution_order) < len(self.tasks_config):
            return {
                "status": "DEADLOCK_DETECTED",
                "execution_order": []
            }
        
        return {
            "status": "SUCCESS",
            "execution_order": execution_order
        }
        
            
if __name__ == "__main__":
    tasks_config = {
        "GENERATE_DOC": [],
        "VERIFY_CREDIT": ["GENERATE_DOC"],
        "APPROVE_LOAN": ["VERIFY_CREDIT"],
        "DISBURSE_FUNDS": ["APPROVE_LOAN"]
    }

    scheduler = SOPTaskScheduler(tasks_config)
    print("Valid Order Result:", scheduler.get_execution_order())

    cyclic_tasks = {
        "STEP_A": ["STEP_C"],
        "STEP_B": ["STEP_A"],
        "STEP_C": ["STEP_B"]
    }

    cyclic_scheduler = SOPTaskScheduler(cyclic_tasks)
    print("Cyclic Result:", cyclic_scheduler.get_execution_order())
