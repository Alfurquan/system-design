import time
import threading
from store import Store
from leader import Leader
from dataclasses import dataclass

class Follower:
    def __init__(self, name):
        self.name = name
        self.last_timestamp = 0
        self.store: Store = Store()
        self.active = True
        self.condition = threading.Condition()

    def replicate_forever(self, leader: Leader, delay: int = 1):
        while True:
            with self.condition:
                while not self.active:
                    print(f"[{self.name}] Paused (crashed). Waiting to recover...")
                    self.condition.wait()

            logs = leader.get_log_since(self.last_timestamp)
            for entry in logs:
                time.sleep(delay)
                self.store.put(entry.key, entry.value)
                self.last_timestamp = entry.timestamp
                print(f"[{self.name}] Replicated {entry}")

            time.sleep(0.5)  # poll again after short wait

    def crash(self):
        with self.condition:
            self.active = False
            print(f"[{self.name}] Simulating crash at ts={self.last_timestamp}")

    def recover(self):
        with self.condition:
            self.active = True
            print(f"[{self.name}] Recovered and resuming replication")
            self.condition.notify_all()

    def read(self, key: str) -> int:
        print(f"[{self.name}] Read {key}")
        return self.store.get(key)