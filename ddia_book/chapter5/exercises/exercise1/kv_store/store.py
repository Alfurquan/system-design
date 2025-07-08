from typing import Dict

class Store:
    def __init__(self):
        self.items: Dict[str, int] = {}
        
    def put(self, key: str, value: int) -> None:
        self.items[key] = value

    def get(self, key: str) -> int:
        return self.items.get(key, None)