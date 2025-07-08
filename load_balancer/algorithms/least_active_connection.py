from typing import List
from .server import Server, ServerStatus
import random

class LeastActiveConnection:
    """
    Load Balancing Algorithm: Least Active Connection
    This algorithm selects the server with the least number of active connections.
    """

    def __init__(self, servers: List[Server]):
        self.servers = servers

    def select_server(self) -> Server:
        """
        Selects the server with the least number of active connections.
        """
        active_servers = [s for s in self.servers if s.status == ServerStatus.ACTIVE]
        if not active_servers:
            raise ValueError("No active servers available")
        
        min_connections = min(s.active_connections for s in active_servers)
        least_loaded = [s for s in active_servers if s.active_connections == min_connections]

        selected_server = random.choice(least_loaded)
        selected_server.active_connections += 1 
        return selected_server