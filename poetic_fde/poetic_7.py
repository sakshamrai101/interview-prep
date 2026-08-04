"""
    Pattern 4: Binary Search on Answer/Boundary Search 

    Context:
    Your system processes batched API requests or SOP executions. You need to find the minimum rate limit threshold or maximum batch size 
    that satisfies given system condition without blowing up memory or exceeding execution timeouts.

    Requirements:

    1. Implement a class RateLimitOptimizer.

    2. Implement a method find_min_sustainable_rate(min_rate: int, max_rate: int, target_latency_ms: int) -> int.

    3. Use Binary Search over the rate range [min_rate, max_rate].

    4. Use a provided mock evaluation helper self.simulate_latency(rate: int) -> int to test if a given rate stays under target_latency_ms.

    5. Return the maximum rate where simulate_latency(rate) <= target_latency_ms. If even min_rate exceeds the target, return -1.


"""

class RateLimitOptimizer:

    def simulate_latency(self, rate: int) -> int:
        """
        Mock latency simulation
        Latency (ms) increases as rate increases 
        Example: rate=500 -> 200ms latency 

        """
        return int(0.4 * rate)
    def find_max_sustainable_rate(self, min_rate: int, max_rate: int, target_latency_ms: int) -> int:

        l = min_rate
        r = max_rate
        best_rate = -1 # default if even min_rate exceeds target latency 

        while l <= r:
            mid = (l + r) // 2
            current_latency = self.simulate_latency(mid)

            # Check if this rate is within legacy bounds 
            if current_latency <= target_latency_ms:
                best_rate = mid # record valid state 
                l = mid + 1    # try searching higher rates on the side 
            else:
                r = mid - 1    # Rate too agressive, search smaller ones

        return best_rate 
if __name__ == "__main__":
    optimizer = RateLimitOptimizer()

    min_rate = 100
    max_rate = 1000
    target_latency = 250

    # For rate * 0.4, max rate under 250ms latency is 625 (625 * 0.4 = 250ms)
    result = optimizer.find_max_sustainable_rate(min_rate, max_rate, target_latency)
    print(f"Maximum sustainable rate under {target_latency}ms latency:", result)
    print(f"Verified Latency at rate {result}: {optimizer.simulate_latency(result)}ms")
    
