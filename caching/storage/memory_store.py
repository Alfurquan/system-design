from typing import Dict
from .store import Store, K, V
from exceptions.exception import NotFoundError, CacheFullError

class MemoryStore(Store[K, V]):
    """
    Concrete implementation of Store using an in-memory dictionary.
    """
    def __init__(self, capacity: int):
        self._store: Dict[K, V] = {}
        self._capacity = capacity

    def get(self, key: K) -> V:
        if key not in self._store:
            raise NotFoundError(f"Key {key!r} not found in store.")
        return self._store[key]

    def put(self, key: K, value: V) -> None:
        if len(self._store) >= self._capacity:
            raise CacheFullError("Store capacity exceeded.")
        self._store[key] = value

    def delete(self, key: K) -> None:
        if key not in self._store:
            raise NotFoundError(f"Key {key!r} not found in store.")
        del self._store[key]
