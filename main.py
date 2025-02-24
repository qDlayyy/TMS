from src.sequental_solutions import math_sequentially, get_url_sequentially
from src.threading_solutions import math_threading, get_urls_threading
from src.multiprocessing_solutions import math_multiprocessing, get_url_multiprocessing


def data_analysis(*args):
    sorted_data_list = sorted(list(args), key=lambda inner_tuple: inner_tuple[1])
    
    print(
        f'\nThe fastest is "{sorted_data_list[0][0]}" method. Estimated time: {sorted_data_list[0][1]:.4f} sec.',
        f'A bit slower is "{sorted_data_list[1][0]}" method. Estimated time: {sorted_data_list[1][1]:.4f} sec.',
        f'The slowest is "{sorted_data_list[2][0]}" method. Estimated time: {sorted_data_list[2][1]:.4f}sec.',
        sep='\n'
    )


def main():
    list_of_args = [23423424, 23123223, 44234244]

    list_of_urls = [
        'https://easypanel.io/',
        'https://www.git-tower.com/mac',
        'https://www.spacex.com/',
        'https://www.bbc.com/weather/2643743',
        'https://www.manutd.com/',
        'https://znwr.ru/',
        'https://www.zara.com/by/ru/',
        'https://www.bsuir.by/'
    ]

    print('\n~ MATH TASKS ~')
    print(f'List of data: {list_of_args}')
    sequentially_data = math_sequentially(list_of_args)
    threading_data = math_threading(list_of_args)
    multiprocessing_data = math_multiprocessing(list_of_args)
    data_analysis(sequentially_data, threading_data, multiprocessing_data)

    print('\n\n~ GET-REQUEST TASKS ~')
    print(f'Amount of urls: {len(list_of_urls)}')
    sequentially_data = get_url_sequentially(list_of_urls=list_of_urls)
    threading_data = get_urls_threading(list_of_urls=list_of_urls)
    multiprocessing_data = get_url_multiprocessing(list_of_urls=list_of_urls)
    data_analysis(sequentially_data, threading_data, multiprocessing_data)


if __name__ == "__main__":
    main()
    
