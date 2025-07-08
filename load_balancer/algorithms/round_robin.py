from typing import List
from .server import Server,ServerStatus

class RoundRobin:
    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.current_index = -1
    
    def select_server(self) -> Server:
        self.servers = [s for s in self.servers if s.status == ServerStatus.ACTIVE]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return self.servers[self.current_index]