from time import time


def timer(func):

    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        print("{} cost: {:.4f}s".format(func.__name__, end-start))
    return wrapper
