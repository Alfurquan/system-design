from dataclasses import dataclass
from typing import List
from store import Store


@dataclass
class Log:
    op: str
    key: str
    value: int
    timestamp: int

class Leader:
    def __init__(self):
        self.store: Store = Store()
        self.timestamp = 0
        self.logs: List[Log] = []

    def write(self, key: str, value: int) -> int:
        self.timestamp += 1
        self.store.put(key, value)
        print(f"[Leader] Set {key}={value} at ts={self.timestamp}") 
        self.logs.append(Log(op="set", key=key, value=value, timestamp=self.timestamp))       
        return self.timestamp

    def read(self, key: str) -> int:
        return self.store.get(key)

    def get_log_since(self, last_ts: int) -> List[Log]:
        return [entry for entry in self.logs if entry.timestamp > last_ts]