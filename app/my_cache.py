from collections import OrderedDict

# Custom exception to raise when the cache is full
class FullCache(Exception):
    def __init__(self, message):
        super().__init__(message)

# My cache class based on OrderedDict
class MyCache(OrderedDict):
    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size
        self.size = 0

    def __setitem__(self, key, value):
        # If the cache is full, raise an exception
        if self.size == self.max_size:
            raise FullCache("Cache is full")
        super().__setitem__(key, value)
        self.size = min(self.size + 1, self.max_size)

    def __delitem__(self, key):
        super().__delitem__(key)
        self.size = max(0, self.size - 1)

    def popitem(self, last = True):
        self.size = max(0, self.size - 1)
        return super().popitem(last)
