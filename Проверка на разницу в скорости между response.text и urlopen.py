import re
import statistics
import time
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

# Экспериментальная ссылка (пробел в номере страницы ссылки нужен "page= ") для того, что бы его заменить на цифру
link_vivo = 'https://www.mediapark.uz/products/category/40?brand%5B%5D=125&price_min=0&price_max=20550000&page= '
# Количество шагов
w = 10

# Функция по проверки скорости работы requests.get
def check_sr_arf_response(link, w):
    # Лист для сохранения количества времени каждого выполненного шага
    list_respons = []

    # Номер страницы
    t = 1

    # Цикл будет продолжаться пока номер страницы не будет равен числу, которое вы ввели в начале программы
    while t <= w:
        # Сайт может дать ошибку из-за большого количества запросов
        try:
            # Замена пробела на номер страницы
            link_and_number = re.sub(r'\s', str(t), link)

            # Начало подсчёта времени работы
            start_time = time.time()

            response = requests.get(link_and_number)
            a = BeautifulSoup(response.text, 'lxml')
            aa = a.find('div', {'class': 'goods-section-right-blocks'})
            aaa = aa.find_all('span', {'class': 'car-block-titile'})

            for name_img in aaa:
                name = name_img.text

            # Завершаем подсчёт
            end_time = time.time()

            # Записываем время работы в лист
            sr = end_time - start_time
            list_respons.append(sr)

            # Пишем на каком этапе программа
            print(t)
            # Прибавляем номер страницы
            t += 1
        # Если будет ошибка сайта, то начинаем подсчёт заново
        except:
            sr, t = check_sr_arf_response(link, w)
            print(f'response: {sr} секунд в среднем за {t} запросов')

    mean_value = 00000
    try:
        mean_value = statistics.mean(list_respons)
        list_respons.clear()
    except:
        sr, t = check_sr_arf_urlopen(link, w)
        print(f'ОШИБКА urlopen: {sr} секунд в среднем за {t} запросов')
        list_respons.clear()

    return mean_value, t


def check_sr_arf_urlopen(link, w):
    list_urlopen = []
    t = 1
    while t <= w:
        try:
            link_and_number = re.sub(r'\s', str(t), link)

            start_time = time.time()
            html = urlopen(link_and_number)
            b = BeautifulSoup(html, 'lxml')
            bb = b.find('div', {'class': 'goods-section-right-blocks'})
            bbb = bb.find_all('span', {'class': 'car-block-titile'})
            for name_img in bbb:
                name = name_img.text
            end_time = time.time()
            sr = end_time - start_time
            list_urlopen.append(sr)
            print(t)
            t += 1
        except:
            sr, t = check_sr_arf_urlopen(link, w)
            print(f'ОШИБКА urlopen: {sr} секунд в среднем за {t} запросов')

    mean_value = 00000
    try:
        mean_value = statistics.mean(list_urlopen)
        list_urlopen.clear()
    except:
        sr, t = check_sr_arf_urlopen(link, w)
        print(f'ОШИБКА urlopen: {sr} секунд в среднем за {t} запросов')
        list_urlopen.clear()

    return mean_value, t


sr, t = check_sr_arf_response(link_vivo, w)
print(f'response: {sr} секунд в среднем за {t} запросов')

sr, t = check_sr_arf_urlopen(link_vivo, w)
print(f'urlopen: {sr} секунд в среднем за {t} запросов')
