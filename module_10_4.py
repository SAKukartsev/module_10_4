#coding: utf-8
from threading import Thread
import queue
from time import sleep
from random import randint


class Table:
    def __init__(self, number=1):
        self.number = number
        self.guest = None


class Guest(Thread):

    def __init__(self, name=''):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:

    def __init__(self, *tables):
        super().__init__()
        self.tables = tables
        self.queue_guest = queue.Queue()
        print(f'       Кафе открыто!\n К вашим услугам {len(tables)} столов!\n Всем приятного аппетита!')

    def guest_arrival(self, *guests):
        for guest in guests:
            cnt = 0
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}.')
                    cnt = 0
                    break
                else:
                    cnt += 1
            if cnt > 0:
                self.queue_guest.put(guest)
                print(f'{guest.name} в очереди.')

    def discuss_guests(self):
        cnt = 0
        while not self.queue_guest.empty() or cnt != len(tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла). Cтол номер {table.number} свободен')
                        table.guest = None
                        cnt += 1
                else:
                    if not self.queue_guest.empty():
                        table.guest = self.queue_guest.get()
                        table.guest.start()
                        print(f'{table.guest.name} вышел из очереди и сел(-а) за стол номер {table.number}.')
                        cnt -= 1
        print(f'Количество свободных столов {cnt}.\n      Кафе закрыто!')


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()