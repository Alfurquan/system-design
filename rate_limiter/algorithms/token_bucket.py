import time
import threading
from collections import defaultdict

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: int):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = defaultdict(lambda: {'tokens': capacity, 'last_checked': time.time()})
        self.lock = threading.Lock()

    def allow_request(self, key: str) -> bool:
        with self.lock:
            now = time.time()
            bucket = self.buckets[key]
            time_passed = now - bucket['last_checked']
            refill = time_passed * self.refill_rate
            bucket['tokens'] = min(self.capacity, bucket['tokens'] + refill)
            bucket['last_checked'] = now
    
            if bucket['tokens'] >= 1:
                bucket['tokens'] -= 1
                return True
            return False