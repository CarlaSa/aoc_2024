from time import perf_counter_ns


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