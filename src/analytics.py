# from collections import defaultdict
import os
import json


class Analytics():
    def __init__(self):
        super().__init__()
        self._home_dir = os.path.expanduser("~")
        # self._analytics_data = defaultdict(lambda: defaultdict(int))
        self._path = "/.config/blind-typing/analyticsData.json"
        try:
            with open(f"{self._home_dir}{self._path}", "r") as file:
                self._analytics_data = json.load(file)
        except IOError:
            with open(f"{self._home_dir}{self._path}", "w") as _:
                self._analytics_data = {}

    def set_key(self, correct_symbol, key):
        """
            Добавляет опечатку в объект
            Args:
                str: correct_symbol: Символ который должен быть
                str: key: Символ что ввел пользователь
        """
        if correct_symbol not in key:
            if correct_symbol not in self._analytics_data:
                self._analytics_data[correct_symbol] = {}
            if key not in self._analytics_data[correct_symbol]:
                self._analytics_data[correct_symbol][key] = 0
            self._analytics_data[correct_symbol][key] += 1

    def final(self):
        """
            Сохраняет изменения
        """
        with open(
                  f"{self._home_dir}/{self._path}",
                  "w",
                  encoding="utf-8"
              ) as file:
            json.dump(self._analytics_data, file, ensure_ascii=False, indent=4)

    def get_key(self):
        """
            Возвращает данные аналитики.
            Returns:
                dict: Словарь с данными об ошибках ввода.
        """
        return self._analytics_data


if __name__ == "__main__":
    JSON = {
        "a": {
            "w": 1,
            "q": 3,
        },
        "b": {
            "s": 2,
            "f": 5
        }
    }

    anal = Analytics()
    for _ in range(10):
        anal.set_key("a", "s")
        anal.set_key("t", "e")

    for s in anal.get_key():
        if s not in JSON:
            JSON[s] = {}
        for a in anal.get_key()[s]:
            if a not in JSON[s]:
                JSON[s][a] = 0
            JSON[s][a] += anal.get_key()[s][a]

    print(JSON)
