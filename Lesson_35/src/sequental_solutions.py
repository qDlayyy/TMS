import math
import time
import requests


def calculate_sqrt_sum(upper_number):
    result = sum(math.sqrt(number) for number in range(1, upper_number + 1))

    return result


def math_sequentially(list_of_args):
    start = time.time()
    results = list(map(calculate_sqrt_sum, list_of_args))
    estimated_time = time.time() - start

    return ('Sequentially', estimated_time)


def get_url_sequentially(list_of_urls):
    start = time.time()
    try:
        result = list(map(requests.get, list_of_urls))
    
    except Exception as e:
        print(f'Error in default request: {e}')
    estimated_time = time.time() - start

    return ('Sequentially', estimated_time)
