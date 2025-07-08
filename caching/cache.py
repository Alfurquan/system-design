from typing import TypeVar, Generic, Optional, Dict
from storage.store import Store
from policies.eviction_policy import EvictionPolicy
from exceptions.exception import CacheFullError
import time

K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    """
    Cache class to store and retrieve key-value pairs.
    """
    def __init__(self, store: Store[K, V], eviction_policy: EvictionPolicy[K], ttl_seconds: Optional[int] = None):
        """
        Initialize the cache with a store and an eviction policy.
        
        Args:
            store: An instance of a store (e.g., MemoryStore).
            eviction_policy: An instance of an eviction policy (e.g., LRU).
            ttl_seconds: Optional time-to-live for cache entries in seconds.
        """
        self._store = store
        self._eviction_policy = eviction_policy
        self._ttl_seconds = ttl_seconds
        self._key_timestamp: Dict[K, float] = {}

    def get(self, key: K):
        """
        Retrieve a value from the cache by key.
        
        Args:
            key: The key to retrieve the value for.
        
        Returns:
            The value associated with the key.
        """
        now = time.time()
        if self._ttl_seconds is not None:
            if key in self._key_timestamp:
                if now - self._key_timestamp[key] > self._ttl_seconds:
                    self._store.delete(key)
                    self._eviction_policy.record_access(key)
                    self._key_timestamp.pop(key, None)
                    raise KeyError(f"Key '{key}' has expired and been removed from the cache.")
            else:
                raise KeyError(f"Key '{key}' not found in cache.")
        value = self._store.get(key)
        self._eviction_policy.record_access(key)
        return value

    def put(self, key: K, value: V):
        """
        Store a key-value pair in the cache.
        
        Args:
            key: The key to store.
            value: The value to associate with the key.
        """
        try:
            now = time.time()
            self._store.put(key, value)
            self._eviction_policy.record_access(key)
            self._key_timestamp[key] = now
        except CacheFullError:
            evicted_key = self._eviction_policy.evict()
            self._store.delete(evicted_key)
            self._key_timestamp.pop(evicted_key, None)
            self._store.put(key, value)
            self._eviction_policy.record_access(key)
            self._key_timestamp[key] = now