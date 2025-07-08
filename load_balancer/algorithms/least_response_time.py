import random
from typing import List
from .server import Server, ServerStatus

class LeastResponseTime:
    """
    Load balancing algorithm that selects the server with the least response time.
    """

    def __init__(self, servers: List[Server]):
        self.servers = servers

    def select_server(self) -> Server:
        """
        Selects the server with the least response time.
        """
        active_servers = [s for s in self.servers if s.status == ServerStatus.ACTIVE]
        if not active_servers:
            raise ValueError("No active servers available")

        min_response_time = min(s.response_time for s in active_servers)
        least_loaded = [s for s in active_servers if s.response_time == min_response_time]
        return random.choice(least_loaded)