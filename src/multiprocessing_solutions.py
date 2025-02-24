import multiprocessing
import time
import math
import requests

def calculate_sqrt_sum(upper_number):
    result = sum(math.sqrt(number) for number in range(1, upper_number + 1))

    return result


def math_multiprocessing(list_of_args):
    start = time.time()
    with multiprocessing.Pool() as pool:
        results = pool.map(calculate_sqrt_sum, list_of_args)

    estimated_time = time.time() - start

    return ('Multiprocessing', estimated_time)


def get_url_multiprocessing(list_of_urls):
    start = time.time()
    try:
        with multiprocessing.Pool(processes=8) as pool:
            data = pool.map(requests.get, list_of_urls)

    except Exception as e:
        print(f'Error in multiprocessing request: {e}')
    
    estimated_time = time.time() - start
    
    return ('Multiprocessing', estimated_time)