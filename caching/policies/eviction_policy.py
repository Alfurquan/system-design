from abc import ABC, abstractmethod
from typing import TypeVar, Generic

K = TypeVar('K')

class EvictionPolicy(Generic[K], ABC):
    """
    Abstract base class for eviction policies in a caching system.
    """
    
    @abstractmethod
    def evict(self) -> K:
        """
        Evict a key from the cache based on the policy.
        
        Returns:
            The key that was evicted.
        """
        pass

    @abstractmethod
    def record_access(self, key: K) -> None:
        """
        Record an access to a key, updating the policy state accordingly.
        
        Args:
            key: The key that was accessed.
        """
        pass

    @abstractmethod
    def remove_key(self, key: K) -> None:
        """
        Optional: Remove a key manually from eviction tracking.
        """
        pass