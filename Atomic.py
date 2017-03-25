import threading

class AtomicCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.count = 0

    def increment(self):
        with self.lock:
            self.count += 1

class AtomicSum:
    def __init__(self):
        self.lock = threading.Lock()
        self.sum = 0

    def add(self, value):
        with self.lock:
            self.sum += value