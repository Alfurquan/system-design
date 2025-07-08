import random
import threading
from typing import List
from leader import Leader
from follower import Follower

class KVStore:
    def __init__(self):
        self.leader = Leader()
        self.followers: List[Follower] = [Follower("follower1"), Follower("follower2"), Follower("follower3")]
        #self.followers: List[Follower] = [Follower("follower1")]
        for follower in self.followers:
            self.start_replication_loop(follower, self.leader)

    def write(self, key: str, value: int):
        self.leader.write(key, value)

    def read(self, key: str) -> int:
        index = random.randint(0, len(self.followers) - 1)
        print(f"Reading from {self.followers[index].name}")
        return self.followers[index].read(key)

    def start_replication_loop(self, follower: Follower, leader: Leader):
        def loop():
            while True:
                follower.replicate_forever(leader, delay=1)
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def crash_follower(self, follower_name: str):
        for follower in self.followers:
            if follower.name == follower_name:
                follower.crash()
                return
    
    def recover_follower(self, follower_name: str):
        for follower in self.followers:
            if follower.name == follower_name:
                follower.recover()
                return
