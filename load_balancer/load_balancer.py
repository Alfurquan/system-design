import threading
import time
from typing import List, Callable, Optional
from algorithms.server import Server, ServerStatus
from algorithms.round_robin import RoundRobin
from algorithms.least_active_connection import LeastActiveConnection
from algorithms.weighted_round_robin import WeightedRoundRobin
from algorithms.consistent_hashing import ConsistentHashing


class StrategyType:
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    CONSISTENT_HASH = "consistent_hash"

class LoadBalancer:
    def __init__(self, servers: List[Server], strategy: str = StrategyType.ROUND_ROBIN):
        self.servers = servers
        self.strategy_name = strategy
        self.strategy = self._get_strategy(strategy)
        self.health_check_thread: Optional[threading.Thread] = None
        self.stop_health_checks = threading.Event()

    def _get_strategy(self, strategy: str):
        if strategy == StrategyType.ROUND_ROBIN:
            return RoundRobin(self.servers)
        elif strategy == StrategyType.WEIGHTED_ROUND_ROBIN:
            return WeightedRoundRobin(self.servers)
        elif strategy == StrategyType.LEAST_CONNECTIONS:
            return LeastActiveConnection(self.servers)
        elif strategy == StrategyType.CONSISTENT_HASH:
            return ConsistentHashing(self.servers)
        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

    def set_strategy(self, strategy: str):
        self.strategy_name = strategy
        self.strategy = self._get_strategy(strategy)

    def get_server(self, key: Optional[str] = None) -> Server:
        if self.strategy_name in {StrategyType.CONSISTENT_HASH}:
            if key is None:
                raise ValueError(f"{self.strategy_name} requires a key")
            return self.strategy.select_server(key)
        return self.strategy.select_server()

    def add_server(self, server: Server):
        self.servers.append(server)
        self._refresh_strategy()

    def remove_server(self, server_id: str):
        self.servers = [s for s in self.servers if s.id != server_id]
        self._refresh_strategy()

    def set_server_status(self, server_id: str, status: str):
        for s in self.servers:
            if s.id == server_id:
                s.status = status
                break
        self._refresh_strategy()

    def _refresh_strategy(self):
        self.set_strategy(self.strategy_name)

    def start_health_checks(self, check_function: Callable[[Server], bool], interval: float = 5.0):
        def health_loop():
            while not self.stop_health_checks.is_set():
                for server in self.servers:
                    healthy = check_function(server)
                    server.status = ServerStatus.ACTIVE if healthy else ServerStatus.INACTIVE
                self._refresh_strategy()
                time.sleep(interval)

        self.stop_health_checks.clear()
        self.health_check_thread = threading.Thread(target=health_loop, daemon=True)
        self.health_check_thread.start()

    def stop_health_checks(self):
        self.stop_health_checks.set()
        if self.health_check_thread:
            self.health_check_thread.join()
