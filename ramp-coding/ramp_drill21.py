""" In memory, api tracking """

class RateLimiterCache:
    def __init__(self, max_requests: int, window_size: int):
        """
        max_requests: Maximum allowed calls inside the timeframe 
        window_size: The rolling window length in seconds 
        """

        self.max_requests = max_requests
        self.window_size = window_size

        # Primary state storage: {user_id -> list of integer timestamps}
        self.user_history = {}

    def is_request_allowed(self, user_id: str, current_time: int) -> bool:
        """
        Evaluates user history, evicts stale timestamps,
        and returns True if the request can proceed safely.

        """

        # 1. Initialize an empty list if this user has never been seen before 
        if user_id not in self.user_history:
            self.user_history[user_id] = []
        
        history = self.user_history[user_id]

        # Calculate the boundary line for our active rolling window 
        window_boundary = current_time - self.window_size

        # 2. THE EVICTION LOOP: Remove timestamps that expired before the boundary 
        # While the list has elements and the oldest timestamp is out of bounds, pop it!

        while history and history[0] <= window_boundary:
            history.pop(0) # Removes the oldest element from the front 
        
        # Evaluate threshold: Check if user has room for another request
        if len(history) < self.max_requests:
            history.append(current_time)
            return True 
        
        return False 