import os
import json


class Analytics():
    def __init__(self):
        super().__init__()
        self._home_dir = os.path.expanduser("~")
        self._analytics_data = {}

    def file_while(self):
        path = "/.config/blind-typing/analyticsDate/analyticsData.json"
        try:
            with open(f"{self._home_dir}{path}", "r") as file:
                self._analytics_data = json.loads(file)
        except IOError:
            with open(f"{self._home_dir}/{path}", "r") as file:
                self._analytics_data = file

    def set_key(self, correct_symbol, key):
        """
            Добавляет опечатку в объект
            Args:
                str: correct_symbol: Символ который должен быть
                str: key: Символ что ввел пользователь
        """
        self._analytics_data[correct_symbol][key] += 1

    def get_key(self):
        """
            Возвращает данные аналитики.

            Returns:
                dict: Словарь с данными об ошибках ввода.
        """
        return self._analytics_data


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
