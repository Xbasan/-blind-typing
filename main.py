#!/usr/bin/env python3

"""
main.py

Тренажёр набора текста с использованием библиотеки curses.
В нём есть главное меню, тесты на скорость набора текста (1 или 30 минут),
проверка ошибок в вводе и подсчёт процента правильных символов.
Программа отображает текст для набора и оценивает точность ввода,
с цветовой индикацией ошибок.
"""


import sys
import time
import curses
import random
import re
from curses import wrapper

# Стартовый экран приложения
LOGO = """
  @@@@@@@@   @@@@@@    @@@@@@   @@@@@@@  @@@@@@@@  @@@  @@@  @@@   @@@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@
  @@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@  @@@@@@@@  @@@  @@@@ @@@  @@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@ 
  @@!       @@!  @@@  !@@         @@!    @@!       @@!  @@!@!@@@  !@@        @@!       @@!  @@@  !@@    
  !@!       !@!  @!@  !@!         !@!    !@!       !@!  !@!!@!@!  !@!        !@!       !@!  @!@  !@! 
  @!!!:!    @!@!@!@!  !!@@!!      @!!    @!!!:!    !!@  @!@ !!@!  !@! @!@!@  @!!!:!    @!@!!@!   !!@@!!  
  !!!!!:    !!!@!!!!   !!@!!!     !!!    !!!!!:    !!!  !@!  !!!  !!! !!@!!  !!!!!:    !!@!@!     !!@!!! 
  !!:       !!:  !!!       !:!    !!:    !!:       !!:  !!:  !!!  :!!   !!:  !!:       !!: :!!        !:! 
  :!:       :!:  !:!      !:!     :!:    :!:       :!:  :!:  !:!  :!:   !::  :!:       :!:  !:!      !:!  
   ::       ::   :::  :::: ::      ::     ::        ::   ::   ::   ::: ::::   :: ::::  ::   :::  :::: ::  
   :         :   : :  :: : :       :      :        :    ::    :    :: :: :   : :: ::    :   : :  :: : :  

                                               ----------
                                               |Hi press|
                                            ----------------
                                            |  1 to start  |
                                            ----------------
                                            |  2 to test   |
                                            ----------------
                                            |  4 to close  |
                                            ----------------
 """


# Генирирует текст
def text_genirate():
    """
        Выполняет чтение из файлов с тестом

        Returns:
            int: длина текта
            str: текст для тринажора
    """

    with open("./text/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()
    res = random.choice(texts)
    return len(res), res


line_length, text = text_genirate()


def new_text_genirate():
    """Обновляет текст"""
    line_length, text = text_genirate()


# Проверка символа на правильность
# text - эталонный текст,
# new_text - пользовательский ввод,
# ind - индекс символа
# Возвращает индекс цвета 2, если символ правильный, и 1, если нет
def text_check(_text, _new_text, ind):
    """
        Выполняет проверку правильности введенного текста.

        Args:
            str: _text: Этолонный текст.
            str: _new_text: Новый введенный текст.
            str: _ind: Номер буквы.
        Returns:
            int: 1 при неправильной буквы 3 при правильном.
    """
    if _text[ind] == _new_text[ind]:
        return 3
    return 1


# Подсчёт процента правильных символов в вводе пользователя
# Возвращает процент правильности
def percentage_correctness(res):
    """
        Проверяет правильности введенного текста
        Args:
            res: Страка веденныя пользавотилем
        Returns:
            int: Процентное соотношение правильности
    """
    per = 0
    for ind, symbol in enumerate(res):
        if text[ind] == symbol:
            per += 1
    return (per / len(text)) * 100


def main(stdscr):
    """
        Отрисовывает стартовый экран приложения
    """
    curses.curs_set(0)  # Отключение отображения курсора
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.clear()
    stdscr.addstr(LOGO)
    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == "1":
            start_spelling(stdscr)  # Запуск треножора
            sys.exit(0)
        elif key == "2":
            menu_sped_test(stdscr)  # Открытие меню тестов
        elif key == "4":
            sys.exit(0)


def text_print(stdscr, _text):
    """
        Пичатает на экране приложения текст
        Args:
            _text: Текст который нужно вывести
    """
    # Расчёт начальной позиции текста
    height, width = stdscr.getmaxyx()
    start_x = (width - 80) // 2
    start_y = height // 2

    x = 0
    y = 0
    for i, _key in enumerate(_text):
        if x >= 80 and _text[i-1] == " ":
            y += 1
            x = 0
        stdscr.addstr(start_y + y - 5, start_x + x, _key)
        x += 1


# Функция начала набора текста
# stdscr - экран curses,
# duration - время теста в секундах
def start_spelling(stdscr, duration=30000):
    """
        Функция начала набора текста
        Args:
            duration: Време длительности теста
        Returns:
            int: Затраченное время
            int: Процент правельности набора
    """
    line_id = 0
    new_text = ""

    height, width = stdscr.getmaxyx()
    start_x = (width - 80) // 2
    start_y = height // 2
    x = 0

    stdscr.clear()
    # Отображение текста
    text_print(stdscr, text)

    start_time = time.time()

    # Цикл для обработки пользовательского вводаc
    while True:
        key = stdscr.getkey()

        # Проверка на завершение времени
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            stdscr.addstr(1, 5,
                          f"Right :: {percentage_correctness(new_text):.2f}%")
            stdscr.addstr(2, 5, "Time to huntc")
            stdscr.addstr(3, 5, "1 : Click to try again")
            stdscr.addstr(4, 5, "2 : Press to return to menu")
            while True:
                key = stdscr.getkey()
                if key == "1":
                    start_spelling(stdscr, duration)
                elif key == "2":
                    menu_sped_test(stdscr)

        index = len(new_text)

        match key:
            case "`":
                sys.exit(0)  # Завершение функции по нажатию `
            case "KEY_BACKSPACE":
                _x = 0
                ln = 0
                # Удаление последнего символа
                new_text = new_text[:-1]
                stdscr.clear()

                text_print(stdscr, text)
                for _index, _key in enumerate(new_text):

                    if _x >= 80 and new_text[_index-1] == " ":
                        ln += 1
                        _x = 0
                    stdscr.addstr(start_y+1+ln,
                                  start_x+_x,
                                  _key,
                                  curses.color_pair(text_check(text,
                                                               new_text,
                                                               _index)))
                    _x += 1
                x = _x

            case _:
                # Добавление символа в пользовательский ввод
                if len(key) == 1 and len(text) != index:
                    new_text += key
                    if line_id > len(text):
                        return [elapsed_time, percentage_correctness(new_text)]

                    if x >= 80 and new_text[index-1] == " ":
                        line_id += 1
                        x = 0
                    stdscr.addstr(start_y+1+line_id,
                                  start_x+x,
                                  key,
                                  curses.color_pair(text_check(text,
                                                               new_text,
                                                               index)))
                    x += 1

                elif len(text) == index:
                    return [elapsed_time, percentage_correctness(new_text)]


# Меню выбора тестов
# stdscr - экран curses
def menu_sped_test(stdscr):
    """
        Отвечает за проведения теста и вывод его результата
    """

    stdscr.clear()
    height, width = stdscr.getmaxyx()

    menu_speed_test = [
        "Select test duration",
        "  1:   1 minute     ",
        "  2:  30 seconds    ",
        "  3:  Come back     ",
        "  4:    Close       "
    ]

    start_x = (width - len(menu_speed_test[0])) // 2
    start_y = height // 2

    try:
        stdscr.addstr(start_y-3, start_x, menu_speed_test[0])
        stdscr.addstr(start_y-1, start_x, menu_speed_test[1])
        stdscr.addstr(start_y, start_x, menu_speed_test[2])
        stdscr.addstr(start_y+1, start_x, menu_speed_test[3])
        stdscr.addstr(start_y+2, start_x, menu_speed_test[4])
    except curses.error:
        stdscr.addstr(1, 0, menu_speed_test[0])
        stdscr.addstr(2, 0, menu_speed_test[1])
        stdscr.addstr(3, 0, menu_speed_test[2])
        stdscr.addstr(4, 0, menu_speed_test[3])
        stdscr.addstr(5, 0, menu_speed_test[4])

    # Цикл для обработки пользовательского ввода в меню
    while True:
        key = stdscr.getkey()

        if key == "1":
            res = start_spelling(stdscr, duration=60)  # Тест на 1 минуту
            stdscr.addstr(2, start_x, f"Right :: {res[1]:.2f}%")
            stdscr.addstr(3, 5, "1 : Click to try again")
            stdscr.addstr(4, 5, "2 : Press to return to menu")

            while True:
                key = stdscr.getkey()
                if key == "1":
                    start_spelling(stdscr, 60)
                elif key == "2":
                    menu_sped_test(stdscr)

        elif key == "2":
            res = start_spelling(stdscr, duration=30)  # Тест на 1 минуту
            stdscr.addstr(2, start_x, f"Right :: {res[1]:.2f}%")
            stdscr.addstr(3, 5, "1 : Click to try again")
            stdscr.addstr(4, 5, "2 : Press to return to menu")

            while True:
                key = stdscr.getkey()
                if key == "1":
                    res = start_spelling(stdscr, 30)  # Перезапуск теста
                    stdscr.addstr(2, start_x, f"Right :: {res[1]:.2f}%")
                    stdscr.addstr(3, 5, "1 : Click to try again")
                    stdscr.addstr(4, 5, "2 : Press to return to menu")
                elif key == "2":
                    menu_sped_test(stdscr)  # Возврат в меню

        elif key == "3":
            main(stdscr)  # Возврат в главное меню
        elif key == "4":
            sys.exit(0)  # Завершение программы
        else:
            stdscr.addstr(1, 1, "What the fuck did you press",
                          curses.color_pair(1))


if __name__ == "__main__":
    wrapper(main)
