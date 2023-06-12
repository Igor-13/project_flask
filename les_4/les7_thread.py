# Задание №7
# � Напишите программу на Python, которая будет находить
# сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами
# от 1 до 100.
# � При решении задачи нужно использовать многопоточность.
# � В каждом решении нужно вывести время выполнения
# вычислений.



from timer import timer, arr
import threading


threads = []
summa = 0
num_threads = 4


def sum_array(start_idx, end_idx):
    global summa
    for i in range(start_idx, end_idx):
        summa += arr[i]


@timer
def get_summa():
    for i in range(num_threads):
        start_idx = i * len(arr) // num_threads
        end_idx = (i + 1) * len(arr) // num_threads
        thread = threading.Thread(target=sum_array, args=(start_idx, end_idx))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    return summa


if __name__ == '__main__':
    get_summa()
