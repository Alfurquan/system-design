from algorithms.sliding_window_counter import SlidingWindowCounter
import time

def main():
    limiter = SlidingWindowCounter(window_size=5, max_request=4)
    key = "user-123"

    for _ in range(8):
        print(limiter.allow_request(key))
        time.sleep(0.1)

    time.sleep(2)
    print(limiter.allow_request(key))

if __name__ == '__main__':
    main()