import hashlib
from bisect import bisect_right
from typing import List, Dict
from .server import Server, ServerStatus


class ConsistentHashing:
    def __init__(self, servers: List[Server], num_replicas = 100):
        self.num_replicas = num_replicas
        self.ring: Dict[int, Server] = {}
        self.sorted_keys: List[int] = []
        self.servers: Dict[str, Server] = {server.id: server for server in servers}
        self.__build_ring(servers)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def __build_ring(self, servers: List[Server]):
        self.ring.clear()
        self.sorted_keys.clear()
        for server in servers:
            if server.status == ServerStatus.ACTIVE:
                for i in range(self.num_replicas):
                    virtual_node = f"{server.id}:{i}"
                    hashed_key = self._hash(virtual_node)
                    self.ring[hashed_key] = server
                    self.sorted_keys.append(hashed_key)
        self.sorted_keys.sort()

    def select_server(self, key: str) -> Server:
        hash_val = self._hash(key)
        index = bisect_right(self.sorted_keys, hash_val) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[index]]

    def add_server(self, server: Server):
        self.servers[server.id] = server
        self.__build_ring(self.servers.values())
    
    def remove_server(self, server: Server):
        if server.id in self.servers:
            del self.servers[server.id]
            self.__build_ring(self.servers.values())

    