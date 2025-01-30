#!/usr/bin/env python3

"""
main.py

Тренажёр набора текста с использованием библиотеки curses.
В нём есть главное меню, тесты на скорость набора текста (1 или 30 минут),
проверка ошибок в вводе и подсчёт процента правильных символов.
Программа отображает текст для набора и оценивает точность ввода,
с цветовой индикацией ошибок.
"""

import re
import sys
import time
import curses
import random
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

                                            ┌──────────────┐
                                            │   Hi press   │
                                            ├──────────────┤
                                            │  1 ─ start   │
                                            ├──────────────┤
                                            │  2 ─ test    │
                                            ├──────────────┤
                                            │  4 ─ close   │
                                            └──────────────┘
 """


# Генирирует текст
def text_genirate(num_words: int):
    """
        Выполняет чтение из файлов с тестом

        Args:
            num_words: Количества слов
        Returns:
            int: длина текта
            str: текст для тринажора
    """

    with open("/home/khamzat/.config/blind-typing/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()
    res_text = random.choice(texts)

    maskc = re.compile(r"\b\w{2,}\b")

    res = " ".join(maskc.findall(res_text)[0:int(num_words)])

    return len(res), res


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
def percentage_correctness(_text, res):
    """
        Проверяет правильности введенного текста
        Args:
            _text: Этолонный текст
            res: Страка веденныя пользавотилем
        Returns:
            int: Процентное соотношение правильности
    """
    per = 0
    for ind, symbol in enumerate(res):
        if _text[ind] == symbol:
            per += 1
    return (per / len(_text)) * 100


def menu_with_results(stdscr, res):
    """
        Отрисовывает прамижктачное меню с результатами
    """
    stdscr.addstr(1, 5, f"Right       :: {res[1]:.2f}%")
    stdscr.addstr(2, 5, f"Print time  :: {res[0]:.2f} s")
    stdscr.addstr(3, 5, f"Corrections :: {res[2]:02}")
    stdscr.addstr(4, 5, "1 : Click to try again")
    stdscr.addstr(5, 5, "2 : Press to return to menu")


# Меню выбора тестов
# stdscr - экран curses
def menuSpedTest(stdscr):
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

        if key == "1":  # Тест на 1 минуту
            menu_with_results(stdscr, start_spelling(stdscr, 60))

            while True:
                key = stdscr.getkey()
                if key == "1":
                    menu_with_results(stdscr, start_spelling(stdscr, 60))
                elif key == "2":
                    menuSpedTest(stdscr)

        elif key == "2":
            menu_with_results(stdscr, start_spelling(stdscr, 30))
            while True:
                key = stdscr.getkey()
                if key == "1":
                    menu_with_results(stdscr, start_spelling(stdscr, 30))
                elif key == "2":
                    menuSpedTest(stdscr)  # Возврат в меню

        elif key == "3":
            main(stdscr)  # Возврат в главное меню
        elif key == "4":
            sys.exit(0)  # Завершение программы
        else:
            stdscr.addstr(1, 1,
                          "What the fuck did you press",
                          curses.color_pair(1))


def text_print(stdscr, _text):
    """
        Пичатает на экране приложения текст
        Args:
            _text: Текст который нужно вывести
    """
    # Расчёт начальной позиции текста
    start_x = (stdscr.getmaxyx()[1] - 80) // 2
    start_y = stdscr.getmaxyx()[0] // 2

    x = 0
    y = 0
    for i, _key in enumerate(_text):
        if x >= 80 and _text[i-1] == " ":
            y += 1
            x = 0
        stdscr.addstr(start_y + y, start_x + x, _key)
        x += 1


def length_selection_menu(stdscr):
    """
        Выводит меню для выбора количесива слов в строке
    """
    MENU = [
        "Сenter the number of words from 1 to 50 and press ENTER to continue"
    ]
    stdscr.clear()
    stdscr.addstr(2, 2, MENU[0])

    lsm = ""
    while True:
        key = stdscr.getkey()

        try:
            if key == "\n":
                if int(lsm) >= 1:
                    return int(lsm)
            elif isinstance(int(key), int):
                if len(lsm) < 2:
                    lsm += key
            stdscr.addstr(3, 3, str(lsm))
        except ValueError:
            pass
            # return int(lsm)


def key_delete(stdscr, _text, n_text, y, x):
    """
        Отвечааете за стерание симвалов

        Ards:
            n_text: Принемает строку из симвалов веденных пользоватилем,
            y: Принемает высота окна,
            x: Принемае длину окна

        Returns:
            new_text: n_text без последнего симвала
            x: позицыя каретки по x
            ln: номер строки
    """
    _x = 0
    ln = 0
    # Удаление последнего символа
    new_text = n_text[:-1]
    stdscr.clear()

    text_print(stdscr, _text)
    for _index, _key in enumerate(new_text):
        if _x >= 80 and new_text[_index-1] == " ":
            ln += 1
            _x = 0
        stdscr.addstr(y+ln,
                      x+_x,
                      _key,
                      curses.color_pair(text_check(_text,
                                                   new_text,
                                                   _index)))
        _x += 1

    return new_text, _x, ln


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

    line_length, text = text_genirate(length_selection_menu(stdscr))
    line_id = 0
    new_text = ""

    corrections = 0

    start_x = (stdscr.getmaxyx()[1] - 80) // 2
    start_y = stdscr.getmaxyx()[0] // 2
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
            return (
                elapsed_time,
                percentage_correctness(text, new_text),
                corrections
            )

        index = len(new_text)

        if key == "``":
            sys.exit(0)  # Завершение функции по нажатию `
        elif key == "KEY_BACKSPACE":
            new_text, x, line_id = key_delete(stdscr, text, new_text, start_y, start_x)
            corrections += 1
        elif len(key) == 1:
            # Добавление символа в пользовательский ввод

            if len(key) == 1 and len(text) != index:
                new_text += key

                if x >= 80 and new_text[index-1] == " ":
                    line_id += 1
                    x = 0

                stdscr.addstr(start_y+line_id,
                              start_x+x,
                              key,
                              curses.color_pair(text_check(text,
                                                           new_text,
                                                           index)))
                x += 1

            elif len(text) == index:
                return (
                    elapsed_time,
                    percentage_correctness(text, new_text),
                    corrections
                )


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
        if key == "1":  # Запуск треножора
            menu_with_results(stdscr, start_spelling(stdscr))
            while True:
                key = stdscr.getkey()
                if key == "1":
                    menu_with_results(stdscr, start_spelling(stdscr))
                elif key == "2":
                    main(stdscr)

        elif key == "2":
            menuSpedTest(stdscr)  # Открытие меню тестов
        elif key == "4":
            sys.exit(0)


if __name__ == "__main__":
    wrapper(main)
