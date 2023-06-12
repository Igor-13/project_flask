import time
from random import randint


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.2f} секунд с результатом {result}")
        return result
    return wrapper


arr = [randint(1, 100) for _ in range(1_000_000)]
