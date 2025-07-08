from abc import ABC, abstractmethod
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')

class Store(Generic[K, V], ABC):
    """
    Abstract base class for a key-value store.
    """
    @abstractmethod
    def get(self, key: K) -> V:
        """
        Retrieve the value associated with the given key.
        """
        pass
    
    @abstractmethod
    def put(self, key: K, value: V) -> None:
        """
        Store the value associated with the given key.
        """
        pass

    @abstractmethod
    def delete(self, key: K) -> None:
        """
        Delete the value associated with the given key.
        """
        pass