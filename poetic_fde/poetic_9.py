from collections import defaultdict
"""
    Problem: Ingestion & Aggregation Engine (Logs to User Metrics)

    Context:
    You are given a list of raw API call logs in JSON format. 
    Write a service that ingests these raw logs and generates an aggregated usage report per user.

    Requirements:
    1. Implement UsageAggregator.

    2. Method ingest_logs(logs: list[dict]) -> None.

    3. Method get_user_summary(user_id: str) -> dict:

    4. Returns total API calls (total_calls).

    5. Average response latency in milliseconds (avg_latency_ms), rounded to 2 decimal places.

    6. Count of errors (error_count), defined as status_code >= 400.

    7. List of distinct endpoint paths accessed (endpoints_accessed).

    8. Handle missing/malformed fields gracefully without crashing.

    raw_logs = [
    {"user_id": "usr_1", "endpoint": "/v1/claim", "status": 200, "latency_ms": 120},
    {"user_id": "usr_1", "endpoint": "/v1/claim", "status": 500, "latency_ms": 300},
    {"user_id": "usr_2", "endpoint": "/v1/auth", "status": 200, "latency_ms": 45},
    {"user_id": "usr_1", "endpoint": "/v1/user", "status": 200, "latency_ms": 80},
    {"user_id": "usr_3", "invalid_log": True} # Corrupted record
    ]

    output:
    get_user_summary("usr_1")
{
    "total_calls": 3,
    "avg_latency_ms": 166.67,
    "error_count": 1,
    "endpoints_accessed": ["/v1/claim", "/v1/user"]
}
"""
class UsageAggregator:

    def __init__(self):
        # Storing aggregated tasks during ingestion is cleaner and more efficient!
        # Structure: { user_id: {"total_calls": 0, "total_latency": 0, "errors": 0, "endpoints": set()} }
        self.user_data = defaultdict(lambda: {
            "total_calls": 0,
            "total_latency": 0,
            "error_count": 0,
            "endpoints": set()
        })

    def ingest_logs(self, logs: list[dict]) -> None:
        """ In-memory ingestion with defensive parsing for malformed logic """
        for log in logs:
            if not isinstance(log, dict):
                continue 
            
        
            user_id = log.get("user_id")
            endpoint = log.get("endpoint")
            status = log.get("status")
            latency_ms = log.get("latency_ms")

            # Validate required fields exist and have valid types 
            if not user_id or not endpoint or status is None or latency_ms is None:
                print(f"Skipping malformed log ....")
                continue 
        
            # Aggregate stats defensively 
            stats = self.user_data[user_id]
            stats["total_calls"] += 1
            stats["total_latency"] += latency_ms
            stats["endpoints"].add(endpoint)

            if isinstance(status, int) and status >= 400:
                stats["error_count"] += 1
    
    def get_user_summary(self, user_id: str) -> dict:
        # Generate the requested user usage report 
        if user_id not in self.user_data:
            return {
                "total_calls": 0,
                "avg_latency_ms": 0.0,
                "error_count": 0,
                "endpoints_accessed": []
            }
        
        stats = self.user_data[user_id]
        total_calls = stats.get("total_calls")
        total_latency = stats.get("total_latency")

        avg_latency_ms = round(total_latency / total_calls, 2) if total_calls > 0 else 0.0

        return {
            "total_calls": total_calls,
            "avg_latency_ms": avg_latency_ms,
            "error_count": stats["error_count"],
            "endpoints_accessed": list(stats["endpoints"])

        }
if __name__ == "__main__":
    raw_logs = [
        {"user_id": "usr_1", "endpoint": "/v1/claim", "status": 200, "latency_ms": 120},
        {"user_id": "usr_1", "endpoint": "/v1/claim", "status": 500, "latency_ms": 300},
        {"user_id": "usr_2", "endpoint": "/v1/auth", "status": 200, "latency_ms": 45},
        {"user_id": "usr_1", "endpoint": "/v1/user", "status": 200, "latency_ms": 80},
        {"user_id": "usr_3", "invalid_log": True}  # Corrupted record
    ]

    aggregator = UsageAggregator()
    aggregator.ingest_logs(raw_logs)

    print("usr_1 Summary:", aggregator.get_user_summary("usr_1"))
    print("usr_3 Summary (Corrupted):", aggregator.get_user_summary("usr_3"))







