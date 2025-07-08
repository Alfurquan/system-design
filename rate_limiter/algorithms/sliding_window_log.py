import time
import threading
from collections import defaultdict, deque

class SlidingWindowLog:
    def __init__(self, window_size: int, max_request: int):
        self.window_size = window_size
        self.max_request = max_request
        self.users_request = defaultdict(lambda: {'request_log': deque()})
        self.lock = threading.Lock()
    
    def allow_request(self, user_ip: str) -> bool:
        with self.lock:
            now = time.time()
            user = self.users_request[user_ip]

            while user['request_log'] and now - user['request_log'][0] >= self.window_size:
                user['request_log'].popleft()
            
            if len(user['request_log']) < self.max_request:
                user['request_log'].append(now)
                return True

            return False