import sys
from typing import Dict, List
from .eviction_policy import EvictionPolicy, K

class LeastFrequentlyUsedPolicy(EvictionPolicy[K]):
    """
    Least Frequently Used (LFU) eviction policy implementation.
    This policy evicts the least frequently accessed key when the cache is full.
    """
    def __init__(self):
        self.freq: Dict[K, int] = {}
        self.freq_list: Dict[int, List[K]] = {}
        self.min_freq: int = sys.maxsize

    def evict(self) -> K:
        """
        Evict the least frequently used key from the cache.
        
        Returns:
            The key that was evicted.
        """
        if self.min_freq == sys.maxsize:
            raise ValueError("No items to evict")
        
        evict_key = self.freq_list[self.min_freq].pop(0)
        if not self.freq_list[self.min_freq]:
            del self.freq_list[self.min_freq]
            self.min_freq += 1
        del self.freq[evict_key]
        return evict_key
    
    def record_access(self, key: K) -> None:
        """
        Record an access to a key, updating the policy state accordingly.
        Args:
            key: The key that was accessed.
        """
        if key not in self.freq:
            self.freq[key] = 1
            self.freq_list.setdefault(1, []).append(key)
            self.min_freq = min(self.min_freq, 1)
        else:
            current_freq = self.freq[key]
            new_freq = current_freq + 1
            self.freq[key] = new_freq
            
            self.freq_list[current_freq].remove(key)
            if not self.freq_list[current_freq]:
                del self.freq_list[current_freq]
                if current_freq == self.min_freq:
                    self.min_freq += 1
            
            self.freq_list.setdefault(new_freq, []).append(key)

    def remove_key(self, key: K) -> None:
        """
        Remove a key manually from eviction tracking.
        
        Args:
            key: The key to remove.
        """
        if key in self.freq:
            current_freq = self.freq[key]
            self.freq_list[current_freq].remove(key)
            if not self.freq_list[current_freq]:
                del self.freq_list[current_freq]
                if current_freq == self.min_freq:
                    self.min_freq += 1
            del self.freq[key]
        else:
            raise KeyError(f"Key '{key}' not found in eviction policy.")