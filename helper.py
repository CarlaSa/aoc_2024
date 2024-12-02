from timeit import default_timer as timer


def time_wrapper(func, space_for_result = 10):
    def wrapper(*args, **kwargs):
        start = timer()
        result = func(*args, **kwargs)
        end = timer()
        time_taken = f"{end - start: .8f} seconds     "

        result_string = f"{func.__name__:10} result: {result:<{space_for_result}} --  {end - start: .8f} seconds      "
        return result_string
    return wrapper