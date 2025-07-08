from typing import List, Optional
from .server import Server, ServerStatus

class WeightedRoundRobin:
    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.current_index = -1
        self.current_weight = 0

    def select_server(self) -> Optional[Server]:
        active_servers = [s for s in self.servers if s.status == ServerStatus.ACTIVE]
        if not active_servers:
            return None

        weights = [s.weight for s in active_servers]

        while True:
            self.current_index = (self.current_index + 1) % len(active_servers)
            if self.current_index == 0:
                self.current_weight -= 1
                if self.current_weight <= 0:
                    self.current_weight = max(weights)
            if weights[self.current_index] >= self.current_weight:
                return active_servers[self.current_index]
