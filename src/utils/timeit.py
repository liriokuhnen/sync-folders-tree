"""Module to simplify timing tracking over a decorator"""

import time
from functools import wraps


def timeit(func):
    """decorator to get time execution of the decorated function"""
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result
    return timeit_wrapper
