from dataclasses import dataclass

class ServerStatus:
    """
    Represents the status of a server.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Server:
    """
    Represents a server in the load balancer system.
    """
    id: str
    name: str
    weight: int
    response_time: float = 0.0
    status: str = ServerStatus.ACTIVE
    active_connections: int = 0


