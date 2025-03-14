# Lesson 38. Aiohttp

> Одновременно можно выполнять запросы как на добавление таска, так и на добавление нового заказа. Предусмотрен слип, который эмулируем длительную обработку.
> Благодаря этому можно одновременно отправить большое количество запросов на создание тасков и заказов, после чего наблюдать их асинхронное выполнение(вывод в консоль).
> 

# Задание №1
- Реализуйте приложение Aiohttp, которое использует asyncio.Queue для организации очереди заданий.
- Пусть "задания" – это простые функции (например, вычисление факториала для числа).
- Создайте несколько воркеров, которые берут задания из очереди и обрабатывают их.
- Реализуйте маршрут /add_task, который добавляет задание в очередь, и маршрут /status, который показывает количество оставшихся заданий.
- Дайте возможность наблюдать за выполнением заданий (вывод в консоль или возвращаемые результаты).

# Задание №2
- Асимптотическая очередь (asyncio.Queue) для хранения заказов.
- Пул воркеров (асинхронных корутин), которые берут заказы из очереди и «обрабатывают» их (например, рассчитывают итоговую стоимость заказа с использованием фиксированного или случайного коэффициента).
- Веб-интерфейс на Aiohttp, предоставляющий два эндпоинта:
- POST /add_order – для добавления нового заказа в очередь (принимает JSON с данными заказа). 
- GET /order_status – для получения статуса (списка обработанных заказов).

