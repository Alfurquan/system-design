from typing import TypeVar, Generic

K = TypeVar('K')

class Node(Generic[K]):
    """
    Node class for the linked list.
    """
    def __init__(self, key: K):
        self.key = key
        self.next = None
        self.prev = None

class DoublyLinkedList(Generic[K]):
    """
    Doubly linked list implementation for managing cache entries.
    """
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_front(self, node: Node[K]) -> None:
        """
        Add a node to the front of the linked list.
        
        Args:
            node: The node to add.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: Node[K]) -> None:
        """
        Remove a node from the linked list.
        
        Args:
            node: The node to remove.
        """
        node.next.prev = node.prev
        node.prev.next = node.next
    
    
