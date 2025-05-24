#!/usr/bin/env python3

"""
main.py

Тренажёр набора текста с использованием библиотеки curses.
В нём есть главное меню, тесты на скорость набора текста (1 или 30 минут),
проверка ошибок в вводе и подсчёт процента правильных символов.
Программа отображает текст для набора и оценивает точность ввода,
с цветовой индикацией ошибок.
"""

import os
import re
import sys
import time
import curses
import random
import asyncio
from curses import wrapper
from analytics import Analytics

# Стартовый экран приложения - ASCII-арт логотипа и меню
LOGO = [
    "@@@@@@@@   @@@@@@    @@@@@@   @@@@@@@  @@@@@@@@  @@@  @@@  @@@   @@@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@ ",
    "@@@@@@@@  @@@@@@@@  @@@@@@@   @@@@@@@  @@@@@@@@  @@@  @@@@ @@@  @@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@ ",
    "@@!       @@!  @@@  !@@         @@!    @@!       @@!  @@!@!@@@  !@@        @@!       @@!  @@@  !@@     ",
    "!@!       !@!  @!@  !@!         !@!    !@!       !@!  !@!!@!@!  !@!        !@!       !@!  @!@  !@!     ",
    "@!!!:!    @!@!@!@!  !!@@!!      @!!    @!!!:!    !!@  @!@ !!@!  !@! @!@!@  @!!!:!    @!@!!@!   !!@@!!  ",
    "!!!!!:    !!!@!!!!   !!@!!!     !!!    !!!!!:    !!!  !@!  !!!  !!! !!@!!  !!!!!:    !!@!@!     !!@!!! ",
    "!!:       !!:  !!!       !:!    !!:    !!:       !!:  !!:  !!!  :!!   !!:  !!:       !!: :!!        !:!",
    ":!:       :!:  !:!      !:!     :!:    :!:       :!:  :!:  !:!  :!:   !::  :!:       :!:  !:!      !:! ",
    " ::       ::   :::  :::: ::      ::     ::        ::   ::   ::   ::: ::::  :: ::::   ::   :::  :::: :: ",
    " :         :   : :  :: : :       :      :         :    ::    :    :: :: :  : :: ::    :   : :  :: : :  ",
    "",
    "╔══════════════╗",
    "║   Hi press   ║",
    "╠══════════════╣",
    "║   1 ─ start  ║",
    "╠══════════════╣",
    "║   2 ─ test   ║",
    "╠══════════════╣",
    "║ 5 ─ Analytic ║",
    "╠══════════════╣",
    "║   4 ─ close  ║",
    "╚══════════════╝"
]

LINE_LENGTH = 80
# Инициализация объекта для сбора аналитики
analy = Analytics()


def text_genirate(num_words: int):
    """
    Генерирует текст для набора из файла с тестами.
    Читает файл test.txt из конфигурационной директории пользователя,
    выбирает случайный текст и обрезает его до указанного количества слов.

    Args:
        num_words: Количество слов для генерации
    Returns:
        tuple: (длина текста, сгенерированный текст)
    """
    home_path = os.path.expanduser("~")
    path = os.path.join(home_path, ".config/blind-typing/test.txt")
    with open(path, "r", encoding="utf-8") as fl:
        texts = fl.readlines()
    res_text = random.choice(texts)
    maskc = re.compile(r"\b[\w.,()\[\]{}]{1,}\b")
    words = maskc.findall(res_text)
    if len(words) >= num_words:
        text_len = random.randint(num_words, len(words))
    else:
        words += maskc.findall(random.choice(texts))[0:len(words)-num_words]
        text_len = random.randint(num_words, len(words))
    res = " ".join(words[text_len-num_words:text_len])
    return len(res), res


def text_check(_text: str, _new_text: str, ind) -> int:
    """
    Проверяет правильность введенного символа.
    Записывает статистику в объект аналитики.

    Args:
        _text: Эталонный текст
        _new_text: Введенный текст пользователя
        ind: Индекс проверяемого символа
    Returns:
        int: код цвета для отображения (
            3 - правильный,
            4 - правильный регистр,
            1 - ошибка)
    """
    analy.set_key(_text[ind], _new_text[ind])
    if _text[ind] == _new_text[ind]:
        return 3
    elif str.upper(_text[ind]) == str.upper(_new_text[ind]):
        return 4
    return 1


def percentage_correctness(_text: str, res: str) -> int:
    """
    Вычисляет процент правильных символов в введенном тексте.

    Args:
        _text: Эталонный текст
        res: Введенный текст пользователя
    Returns:
        float: Процент правильных символов
    """
    per = 0
    for ind, symbol in enumerate(res):
        if _text[ind] == symbol:
            per += 1
    return (per / len(_text)) * 100


def information_about_typos(stdscr):
    """
    Отображает статистику по ошибкам ввода в виде прокручиваемого списка.
    Показывает для каждого символа, какие ошибки делал пользователь
    и их количество.
    """
    stdscr.clear()
    stdscr.keypad(True)

    date = analy.get_key()  # Получение данных аналитики
    lines = []
    intermediate = "╠═════════╬══════════╬═══════╬════════╣"
    # Формирование строк для отображения статистики
    for sim in date:
        sort_sim = dict(
                        sorted(date[sim].items(),
                               key=lambda item: item[1],
                               reverse=True))
        sum_ke = 0
        for i, ke in enumerate(sort_sim):
            s = f"{sum_ke if (len(sort_sim)-1 == i) else ' '}"
            # if date[sim][ke] >= 1:
            lines.append(f"║{sim:^9}║{ke:^10}║{date[sim][ke]:^7}║{s:^8}║")
            sum_ke += date[sim][ke]
        if lines[-1] != intermediate:
            lines.append(intermediate)

    current_line = 0
    max_x, max_y = stdscr.getmaxyx()

    # Цикл отображения с возможностью прокрутки
    while True:
        stdscr.clear()
        stdscr.addstr(0, 1, "  Prev cmds work here too 'q' ",
                      curses.color_pair(2))
        stdscr.addstr(1, 1, "╔═════════╦══════════╦═══════╦════════╗")
        stdscr.addstr(2, 1, "║ Correct ║ Mistyped ║ Count ║ CountS ║")
        stdscr.addstr(3, 1, "╠═════════╬══════════╬═══════╬════════╣")

        # Отображение видимой части списка
        for idx, line in enumerate(lines[current_line: current_line + max_y]):
            try:
                stdscr.addstr(idx + 4, 1, line)
            except curses.error:
                pass

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if current_line > 0:
                current_line -= 1
        elif key == curses.KEY_DOWN:
            if current_line < len(lines) - 2:
                current_line += 1
        elif key in (ord("q"), 27):
            break
    # for inte, sim in enumerate(date):
    #     str_elim = f"{sim} : {dict(
    #                                sorted(
    #                                       date[sim].items(),
    #                                       key=lambda item: item[1],
    #                                       reverse=True)
    #                            )}"
    #     stdscr.addstr(inte+1, 2, str_elim)


def menu_with_results(stdscr, res):
    """
    Отображает меню с результатами теста:
    - Процент правильных символов
    - Время набора
    - Процент исправлений
    """
    cor = (res[2][0] / res[2][1]) * 100

    stdscr.addstr(2, 5, f"Right       :: {res[1]:.2f}%")
    stdscr.addstr(3, 5, f"Print time  :: {res[0]:.2f} s")
    stdscr.addstr(4, 5, f"Corrections :: {cor:.2f}% {res[2][0]}/{res[2][1]}")
    stdscr.addstr(5, 5, "1 : Click to try again")
    stdscr.addstr(6, 5, "2 : Press to return to menu")


def MainMenu(stdscr):
    """
    Отображает главное меню программы с ASCII-артом.
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Центрированное отображение логотипа и меню
    for num, item in enumerate(LOGO):
        print(num)
        start_x = (width - len(item)) // 2
        start_y = height // 2
        stdscr.addstr(start_y+num-12, start_x, item)


async def menuSpedTest(stdscr):
    """
    Отображает меню выбора продолжительности теста:
    - 1 минута
    - 30 секунд
    - Возврат в меню
    - Выход
    - Аналитика
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    menu_speed_test = [
        "Select test duration",
        "  1:   1 minute     ",
        "  2:  30 seconds    ",
        "  3:  Come back     ",
        "  4:    Close       ",
        "  5:  Analytics     "
    ]

    # Центрирование меню
    start_x = (width - len(menu_speed_test[0])) // 2
    start_y = height // 2

    try:
        # Попытка центрированного отображения
        stdscr.addstr(start_y-3, start_x, menu_speed_test[0])
        stdscr.addstr(start_y-1, start_x, menu_speed_test[1])
        stdscr.addstr(start_y, start_x, menu_speed_test[2])
        stdscr.addstr(start_y+1, start_x, menu_speed_test[3])
        stdscr.addstr(start_y+2, start_x, menu_speed_test[4])
        stdscr.addstr(start_y+3, start_x, menu_speed_test[5])
    except curses.error:
        # Если не хватает места, отображаем в верхнем левом углу
        stdscr.addstr(1, 0, menu_speed_test[0])
        stdscr.addstr(2, 0, menu_speed_test[1])
        stdscr.addstr(3, 0, menu_speed_test[2])
        stdscr.addstr(4, 0, menu_speed_test[3])
        stdscr.addstr(5, 0, menu_speed_test[4])
        stdscr.addstr(6, 0, menu_speed_test[5])

    # Обработка выбора пользователя
    while True:
        key = stdscr.getkey()

        if key == "1":    # Тест на 1 минуту
            menu_with_results(stdscr, await start_spelling(stdscr, 60))
            await main_menu_loop(stdscr, 60)
        elif key == "2":  # Тест на 30 секунд
            menu_with_results(stdscr, await start_spelling(stdscr, 30))
            await main_menu_loop(stdscr, 30)
        elif key == "3":  # Возврат в главное меню
            await async_main(stdscr)
        elif key == "4":  # Выход
            sys.exit(0)
        elif key == "5":  # Просмотр аналитики
            information_about_typos(stdscr)
        else:
            stdscr.addstr(1, 1,
                          "What the fuck did you press",
                          curses.color_pair(1))


async def main_menu_loop(stdscr, time: int):
    """
    Цикл обработки ввода в главном меню после завершения теста.
    """
    while True:
        key = stdscr.getkey()
        if key == "1":    # Повторить тест
            menu_with_results(stdscr, await start_spelling(stdscr, time))
        elif key == "2":  # Вернуться в меню тестов
            await menuSpedTest(stdscr)


async def text_print(stdscr, _text: str, pause=False):
    """
    Отображает текст для набора с переносами строк
    (макс. {LINE_LENGTH} символов в строке).
    """
    # Расчёт начальной позиции текста
    start_x = (stdscr.getmaxyx()[1] - LINE_LENGTH) // 2
    start_y = (stdscr.getmaxyx()[0] - 5) // 2
    x = 0
    y = 0
    for i, _key in enumerate(_text):
        if x >= LINE_LENGTH and _text[i-1] == " ":  # Перенос на новую строку
            y += 1
            x = 0
        stdscr.addstr(start_y + y, start_x + x, _key)
        stdscr.refresh()
        x += 1
        # if pause:
        # await asyncio.sleep(0.03)


def length_selection_menu(stdscr):
    """
    Меню выбора количества слов в тесте (от 1 до 99).
    """
    MENU = [
        "Сenter the number of words from 1 to 99 and press ENTER to continue"
    ]
    stdscr.clear()
    stdscr.addstr(2, 4, MENU[0])

    lsm = ""
    while True:
        key = stdscr.getkey()
        try:
            if key == "\n":  # Enter - завершение ввода
                if lsm in ["00", "0"]:
                    lsm = 1
                return int(lsm)
            elif isinstance(int(key), int):  # Ввод цифр
                if len(lsm) < 2:
                    lsm += key
            stdscr.addstr(3, 4, str(lsm))
        except ValueError:
            pass


async def key_delete(stdscr, _text: str, n_text: str, y: int, x: int):
    """
    Обрабатывает удаление символа (Backspace):
    - Удаляет последний символ
    - Перерисовывает текст с учетом изменений
    - Обновляет позицию курсора

    Returns:
        tuple: (новый текст, позиция X, номер строки)
    """
    _x = 0
    ln = 0
    new_text = n_text[:-1]  # Удаление последнего символа
    stdscr.clear()

    stdscr.addstr(1, 5, f"{len(_text)}")
    await text_print(stdscr, _text)
    # Перерисовка введенного текста с подсветкой ошибокc
    for _index, _key in enumerate(new_text):
        if _x >= LINE_LENGTH and new_text[_index-1] == " ":
            ln += 1
            _x = 0
        stdscr.addstr(
                      y + ln,
                      x + _x,
                      _key,
                      curses.color_pair(
                                        text_check(
                                                   _text,
                                                   new_text,
                                                   _index
                                               )
                                    )
                  )
        _x += 1

    return new_text, _x, ln


async def start_spelling(stdscr, duration=30000):
    """
    Основная функция тестирования набора текста.
    Управляет процессом набора, подсчетом времени и статистики.

    Args:
        duration: Продолжительность теста в секундах
    Returns:
        tuple: (затраченное время, процент правильности,
               (кол-во исправлений, длина текста))
    """
    line_length, text = text_genirate(length_selection_menu(stdscr))
    line_id = 0
    new_text = ""
    corrections = 0  # Счетчик исправлений

    start_x = (stdscr.getmaxyx()[1] - LINE_LENGTH) // 2
    start_y = (stdscr.getmaxyx()[0] - 5) // 2
    x = 0

    stdscr.clear()

    stdscr.addstr(1, 5, f"{len(text)}")
    await text_print(stdscr, text, pause=True)

    start_time = time.time()

    # Основной цикл обработки ввода
    while True:
        key = stdscr.getkey()

        # Проверка на завершение времени
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            return (
                elapsed_time,
                percentage_correctness(text, new_text),
                (corrections, len(text))
            )

        index = len(new_text)

        if key == "`":  # Выход по `
            sys.exit(0)
        elif key == "KEY_BACKSPACE":  # Обработка удаления
            new_text, x, line_id = await key_delete(
                                              stdscr,
                                              text,
                                              new_text,
                                              start_y,
                                              start_x
                                          )
            corrections += 1
        elif len(key) == 1:  # Обработка ввода символа
            if key == "\n":
                key = " "    # Замена Enter на пробел

            if len(key) == 1 and len(text) != index:
                new_text += key
                # Перенос строки
                if x >= LINE_LENGTH and new_text[index-1] == " ":
                    line_id += 1
                    x = 0

                # Отображение символа с подсветкой
                stdscr.addstr(start_y+line_id,
                              start_x+x,
                              key,
                              curses.color_pair(text_check(text,
                                                           new_text,
                                                           index)))
                x += 1

            elif len(text) == index:  # Весь текст набран
                analy.final()         # Сохранение статистики
                return (
                    elapsed_time,
                    percentage_correctness(text, new_text),
                    (corrections, len(text))
                )
            stdscr.addstr(1, 10, str(index+1))


async def async_main(stdscr):
    """
    Главная функция, инициализирует curses и запускает главное меню.
    """
    curses.curs_set(0)  # Скрытие курсора
    # Инициализация цветовых пар:
    # 1 - ошибка (зеленый на красном)
    # 2 - хуй знает зачем но без него не работает (черный на белом)
    # 3 - правильный символ (черный на зеленом)
    # 4 - правильный символ, другой регистр (черный на желтом)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    stdscr.clear()
    MainMenu(stdscr)
    stdscr.refresh()

    # Обработка выбора в главном меню
    while True:
        key = stdscr.getkey()
        if key == "1":  # Запуск треножора
            menu_with_results(stdscr, await start_spelling(stdscr))
            while True:
                key = stdscr.getkey()
                if key == "1":    # Повторить
                    menu_with_results(stdscr, await start_spelling(stdscr))
                elif key == "2":  # В главное меню
                    await async_main(stdscr)

        elif key == "2":  # Меню тестов
            await menuSpedTest(stdscr)
        elif key == "4":  # Выход
            sys.exit(0)
        elif key == "5":  # Аналитика
            information_about_typos(stdscr)


def main(stdscr):
    asyncio.run(async_main(stdscr))


if __name__ == "__main__":
    wrapper(main)
