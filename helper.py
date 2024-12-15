import functools
from collections import defaultdict
import random
from time import perf_counter_ns

import numpy as np
from pandas.core.computation.ops import isnumeric


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

def memoized(keywords):
    def actual_memoized(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (kwargs[key] for key in keywords)
            if cache_key in cache:
                return cache[cache_key]
            else:
                result = func(*args, **kwargs)
                cache[cache_key] = result
                return result
        return wrapper
    return actual_memoized



color_codes = {
    "red": '\033[91m',
    "green": '\033[92m',
    "blue": '\033[94m',
    "yellow": '\033[93m',
    "cyan": '\033[96m',
    "magenta": '\033[95m',
    "purple": '\033[96m',
}

def rgb_color_code(r,g,b):
    return f"\033[38;2;{r};{g};{b}m"

def simcmap(string, color):
    if not isinstance(string, str):
        if isinstance(string, bool) or isinstance(string, np.bool_):
            string = f"{str(string):6}"
        elif isnumeric(string):
            string = f"{string:3}"
        else:
            print(type(string))
            raise NotImplementedError

    if color is not None:
        if color in color_codes:
            CSTART = color_codes[color]
        elif len(color) == 3: # rgb
            CSTART = rgb_color_code(*color)
        CEND = '\033[0m'
        repr = CSTART + string + CEND
    else:
        repr = string

    return repr


def np_repr(arr : np.ndarray) -> str:
    representation = ""
    assert len(arr.shape) == 2
    for line in arr:
        representation += " ".join(str(elem) for elem in line)
        representation += "\n"
    return representation


def test_grid():
    string = ""
    step = 40
    for g in range(0, 256, 16):
        for b in range(0, 256, 16):
            for r in range(0, 256, 16):
                string += simcmap("test", (r,g,b))
                string += " "
            string += "\n"
    print(string)

def get_n_colors(n):
    # doesn't have to be good lol
    samples = list()
    for g in range(0, 256, 16):
        for b in range(0, 256, 16):
            for r in range(0, 256, 16):
                samples.append((r,g,b))

    random.shuffle(samples)
    return samples[:n]


def np_repr_unique(arr : np.ndarray) -> str:
    unique_values = np.unique(arr)

    arr_copy = arr.copy()
    if arr_copy.dtype != "object":
        arr_copy = arr_copy.astype("object")
    if len(unique_values) < len(color_codes):
        colors = iter(color_codes.keys())
    else:
        colors = iter(get_n_colors(len(unique_values)))
    for val in unique_values:
        next_color = next(colors, None)
        colored_value = simcmap(val, next_color)
        arr_copy[arr_copy == val] = colored_value
    return np_repr(arr_copy)

def np_color_print(arr : np.ndarray):
    print(np_repr_unique(arr))


def np_print(arr : np.ndarray):
    print(np_repr(arr))

if __name__ == "__main__":
    test_grid()
