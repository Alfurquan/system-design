from algorithms.server import Server, ServerStatus
from load_balancer import LoadBalancer, StrategyType

# Sample servers
servers = [
    Server(id="1", name="A", weight=1),
    Server(id="2", name="B", weight=2),
    Server(id="3", name="C", weight=1),
]

# Health check mock
def mock_health_check(server):
    # Randomly simulate unhealthy servers or use response_time logic
    import random
    return random.choice([True, True, False])  # 2/3 chance of being healthy

lb = LoadBalancer(servers, strategy=StrategyType.CONSISTENT_HASH)

# Start health checks
lb.start_health_checks(mock_health_check, interval=10)

# Simulate requests
for i in range(10):
    server = lb.get_server(f"user-{i}")
    print(f"user-{i} → {server.name}")

# Simulate backend going offline
lb.set_server_status("2", ServerStatus.INACTIVE)
print("Server B marked inactive manually.")

# Add new server
lb.add_server(Server(id="4", name="D", weight=1))

for i in range(10):
    server = lb.get_server(f"user-{i}")
    print(f"user-{i} → {server.name}")
