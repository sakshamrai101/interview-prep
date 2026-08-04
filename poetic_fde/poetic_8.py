"""
    Pattern 5: Sliding Window Search over Streaming Event Logs 

    Context: 
    Your automation pipeline processes a continuous stream of execution event timestamps. 
    To trigger an alert or throttling rule, you need to find the maximum number of events that occurred within any 
    moving window of size $T$ milliseconds, or find the shortest time window that contained at least K consecutive error events.

    Requirements:

    1. Implement a class EventLogSearcher.
    2. Implement a method max_events_in_window(timestamps: list[int], window_size_ms: int) -> int.
    3. The timestamps list is sorted in non-decreasing order (chronological event log).
    4. Use a Sliding Window (Two-Pointer) approach with O(N) time complexity and O(1) extra space.
    5. Return the maximum count of events falling within any inclusive interval [t_{start}, t_{start} + {window\_size\_ms}].
"""

class EventLogSearcher:
    """
    Search Engine for finding peak event frequency within a fixed sliding window.

    """

    def max_events_in_window(self, timestamps: list[int], window_size_ms: int) -> int:
        """
            Calculates the maximum number of events ocurring within any moving window size 'window_size_ms'
        """

        if not timestamps or not window_size_ms:
            return 0
        
        left = 0
        max_count = 0

        for right in range(len(timestamps)):
            while timestamps[right] - timestamps[left] > window_size_ms:
                left += 1
            
            current_window = right - left + 1
            max_count = max(max_count, current_window)
        
        return max_count


if __name__ == "__main__":
    searcher = EventLogSearcher()

    timestamps = [100, 150, 200, 350, 400, 420, 450, 700]
    window_size_ms = 150

    result = searcher.max_events_in_window(timestamps, window_size_ms)
    print(f"Max events in {window_size_ms}ms window:", result)