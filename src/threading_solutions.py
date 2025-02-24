import math
import time
import threading
import concurrent.futures
import requests


def calculate_sqrt_sum(results, upper_number, index):
    result = sum(math.sqrt(number) for number in range(1, upper_number + 1))

    results[index] = result


def math_threading(list_of_args):
    results = [None] * len(list_of_args)
    threads = []
    start = time.time()
    for index, item in enumerate(list_of_args):
        thread = threading.Thread(target=calculate_sqrt_sum, args=(results, item, index))
        threads.append(thread)
        thread.start()
    
    for thr in threads:
        thr.join()

    estimated_time = time.time() - start

    return ('Threading', estimated_time)


def get_urls_threading(list_of_urls):
    start = time.time()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            data = list(executor.map(requests.get, list_of_urls))
    
    except Exception as e:
        print(f'Error in threading request: {e}')
    
    estimated_time = time.time() - start

    return ('Threading', estimated_time)
