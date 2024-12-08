from time import perf_counter_ns

import numpy as np


def time_wrapper(func, space_for_result = 10):
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        result = func(*args, **kwargs)
        end = perf_counter_ns()
        time_elapsed = end - start
        time_elapsed = time_elapsed / 1e9
        result_string = f"{func.__name__:10} result: {result:<{space_for_result}} --  {time_elapsed: .8f} seconds      "
        return result_string
    return wrapper

def memoized(func):
    cache = {}
    def wrapper(*args, **kwargs):
        if args not in cache:
            cache[args] = func(*args, **kwargs)
        return cache[args]
    return wrapper


def simcmap(string, color):
    color_codes = {
            "red": '\033[91m',
            "green": '\033[92m',
            "blue": '\033[94m',
            "yellow": '\033[93m',
            "cyan": '\033[96m',
            "magenta": '\033[95m',
            }
    CSTART = color_codes[color]
    CEND = '\033[0m'
    repr = CSTART + string + CEND
    return repr


def np_repr(arr : np.ndarray) -> str:
    representation = ""
    assert len(arr.shape) == 2
    for line in arr:
        representation += " ".join(str(elem) for elem in line)
        representation += "\n"
    return representation


def np_print(arr : np.ndarray) -> str:
    print(np_repr(arr))