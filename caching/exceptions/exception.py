class NotFoundError(Exception):
    """
    Exception raised when a requested key is not found.
    """
    pass

class CacheFullError(Exception):
    """
    Exception raised when the cache is full and cannot store new items.
    """
    pass

