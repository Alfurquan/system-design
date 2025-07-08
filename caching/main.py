import time
from cache import Cache
from policies.lfu_policy import LeastFrequentlyUsedPolicy
from storage.memory_store import MemoryStore
def main():
    store = MemoryStore[str, str](capacity=3)
    
    eviction_policy = LeastFrequentlyUsedPolicy[str]()
    
    cache = Cache[str, str](store=store, eviction_policy=eviction_policy, ttl_seconds=5)
    try:
        # Add some items to the cache
        cache.put("a", "apple")
        cache.put("b", "banana")
        cache.put("c", "cherry")
        
        # Access an item to update its usage
        print(cache.get("c"))
        print(cache.get("a"))
        time.sleep(6)
        print(cache.get("b"))
        
        cache.put("d", "date")
        
        # Try to get the evicted item
        print(cache.get("c"))
    except Exception as e:
        print(e)

if __name__ == "__main__":
   main()