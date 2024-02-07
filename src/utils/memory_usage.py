"""Module to simplify memory tracking over a decorator"""

import os
from functools import wraps

import humanize
import psutil


def memory_usage(func):
    """decorator to record memory usage of the decorated function"""
    @wraps(func)
    def memory_usage_wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_start = process.memory_info()[0]
        result = func(*args, **kwargs)
        mem_end = process.memory_info()[0]
        natural_size = humanize.naturalsize(mem_end - mem_start)
        print(f"memory usage of {func.__name__}: {natural_size}")
        return result
    return memory_usage_wrapper
