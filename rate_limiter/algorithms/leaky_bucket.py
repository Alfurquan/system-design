from collections import deque, defaultdict
import threading
import time

class LeakyBucket:
    def __init__(self, capacity: int, leak_rate: int):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.buckets = defaultdict(lambda: {'tokens': deque(), 'last_leak': time.time()})
        self.lock = threading.Lock()

    def allow_request(self, key: str) -> bool:
        with self.lock:
            now = time.time()
            bucket = self.buckets[key]
            leak_time = now - bucket['last_leak']
            leaked = int(leak_time * self.leak_rate)
            if leaked > 0:
                for _ in range(min(self.capacity, leaked)):
                    bucket['tokens'].popleft()
                bucket['last_leak'] = now

            if len(bucket['tokens']) < self.capacity:
                bucket['tokens'].append(now)
                return True
            return False