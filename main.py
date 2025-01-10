#!/usr/bin/env python3

import sys
import time
import curses
import random
import re
from curses import wrapper

# Стартовый экран приложения
logo = """
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
    with open("./text/test.txt", "r", encoding="utf-8") as fl:
        texts = fl.readlines()
    time_maskc = re.compile(r".{60,90}\s")
    res = random.choice(texts)
    return len(res), time_maskc.findall(res), res


line_length, text_arr, text = text_genirate()


# Проверка символа на правильность
# text - эталонный текст,
# new_text - пользовательский ввод,
# ind - индекс символа
# Возвращает индекс цвета 2, если символ правильный, и 1, если нет
def text_check(text, new_text, ind):
    if text[ind] == new_text[ind]:
        return 2
    return 1


# Подсчёт процента правильных символов в вводе пользователя
# Возвращает процент правильности
def percentage_correctness(res):
    per = 0
    for ind, symbol in enumerate(res):
        if text[ind] == symbol:
            per += 1
    return (per / len(text)) * 100


def main(stdscr):
    curses.curs_set(0)  # Отключение отображения курсора
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)  # Цветовая ошиби
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Цветовая текста

    stdscr.clear()
    stdscr.addstr(logo)
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


# Функция начала набора текста
# stdscr - экран curses,
# duration - время теста в секундах
def start_spelling(stdscr, duration=30000):
    new_text_full = ""
    line_id = 0
    new_text = ""

    # Расчёт начальной позиции текста
    height, width = stdscr.getmaxyx()
    start_x = (width - len(max(text_arr))) // 2
    start_y = height // 2

    stdscr.clear()
    # Отображение эталонного текста
    for ind, tx in enumerate(text_arr):
        stdscr.addstr(start_y+ind-4, start_x,
                      tx, curses.color_pair(2))

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
        character_number_line = len(new_text_full)

        match key:
            case "`":
                sys.exit(0)  # Завершение функции по нажатию `
            case "KEY_BACKSPACE":
                # Удаление последнего символа
                new_text = new_text[:-1]
                new_text_full = new_text_full[:-1]
                stdscr.clear()

                for ind, tx in enumerate(text_arr):
                    stdscr.addstr(start_y+ind-4, start_x,
                                  tx, curses.color_pair(2))

                if line_id != 0:
                    i = 0
                    for _index, _key in enumerate(new_text_full):
                        if _index >= len(text_arr[i]):
                            stdscr.addstr(start_y+2,
                                          start_x + _index+i,
                                          _key,
                                          curses.color_pair(text_check(
                                                                       text,
                                                                       new_text_full,
                                                                       _index)))
                        else:
                            i +=1
                else:
                    for _index, _key in enumerate(new_text):
                        stdscr.addstr(start_y+2,
                                      start_x + _index,
                                      _key,
                                      curses.color_pair(text_check(
                                                                   text,
                                                                   new_text_full,
                                                                   _index)))
            case _:
                # Добавление символа в пользовательский ввод
                if len(key) == 1 and line_length != index:
                    new_text += key
                    new_text_full += key
                    if len(text_arr[line_id]) > len(new_text):
                        stdscr.addstr(start_y+2+line_id,
                                      start_x+index,
                                      key,
                                      curses.color_pair(text_check(text,
                                                                   new_text_full,
                                                                   character_number_line)))
                    else:
                        line_id += 1
                        if line_id > len(text_arr):
                            return [elapsed_time, percentage_correctness(new_text)]
                        new_text = key
                        index = 0
                        stdscr.addstr(start_y+2+line_id,
                                      start_x+index,
                                      key,
                                      curses.color_pair(text_check(text,
                                                                   new_text_full,
                                                                   character_number_line)))

                elif len(text) == index:
                    return [elapsed_time, percentage_correctness(new_text)]


# Меню выбора тестов
# stdscr - экран curses
def menu_sped_test(stdscr):
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
