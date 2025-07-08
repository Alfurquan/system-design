from typing import Dict
from .eviction_policy import K, EvictionPolicy
from data_structures.linked_list import DoublyLinkedList, Node

class LeastRecentlyUsedPolicy(EvictionPolicy[K]):
    """
    Least Recently Used (LRU) eviction policy implementation.
    This policy evicts the least recently accessed key when the cache is full.
    """
    
    def __init__(self):
        self.list = DoublyLinkedList[K]()
        self.keys: Dict[K, Node[K]] = {}

    def evict(self) -> K:
        """
        Evict the least recently used key from the cache.
        
        Returns:
            The key that was evicted.
        """
        if not self.list.head.next or not self.list.tail.prev:
            raise ValueError("No keys to evict.")
        
        lru_node = self.list.tail.prev
        self.list.remove(lru_node)
        del self.keys[lru_node.key]
        return lru_node.key
    
    def record_access(self, key: K) -> None:
        """
        Record an access to a key, updating the policy state accordingly.
        Args:
            key: The key that was accessed.
        """
        if key in self.keys:
            node = self.keys[key]
            self.list.remove(node)
            self.list.add_to_front(node)
        else:
            node = Node(key)
            self.list.add_to_front(node)
            self.keys[key] = node

    def remove_key(self, key: K) -> None:
        """
        Remove a key manually from eviction tracking.
        
        Args:
            key: The key to remove.
        """
        if key in self.keys:
            node = self.keys[key]
            self.list.remove(node)
            del self.keys[key]
        else:
            raise KeyError(f"Key '{key}' not found in eviction policy.")