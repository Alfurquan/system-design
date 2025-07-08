from kv_store import KVStore
import time

def run():
    store = KVStore()

    store.write("key1", 100)
    store.write("key2", 200)
    time.sleep(0.5)

    store.crash_follower("follower1")

    store.write("key3", 300)
    time.sleep(10)
    store.recover_follower("follower1")
    time.sleep(3)

    print(f"Reading key1: {store.read('key1')}")
    print(f"Reading key2: {store.read('key2')}")

if __name__ == "__main__":
    run()