
import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Function '{}' executed in {:.2f} seconds.".format(func.__name__, execution_time))
        return result
    return wrapper